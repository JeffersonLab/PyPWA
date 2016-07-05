!     =======================================================================
      subroutine ktamplitude(ret,s,t,u,param)
      implicit none
      real    (8) :: s,t,u,param
      complex (8) :: ret
      logical     :: threebody
cf2py intent(out) ret


      threebody = .true.           ! with/ without 3b rescattering effects
      call uploadomega(threebody) ! Upload amplitudes for different Mw=[0.6,0.95] and energy and then interpolate



!      param=1.d0  !parameter that is responsible for the shape
!      s=0.25d0
!      t=0.25d0
!      u=0.048d0 

      call amp(ret,s,t,u,param) ! ret - result which is F(s,t,u) from Eq.(37) (arXiv:1409.7708)
                                ! To get the intensity one has to multiply it by the p-wave phase space P(s,t,u)


!      write(*,*) 's,t,u, ampl',s,t,u,ret
      return
      end subroutine ktamplitude

!     -----------------------------------------------------------------------
      subroutine amp(ret,s,t,u,param)
      implicit none
!     input
      real (8) :: s,t,u,param
!     output
      complex (8) :: ret
!     parameters
      real (8), parameter :: xmp=0.1380386666666667d0 !pion mass
!     internal variables
      real (8) :: momega
      complex (8) :: f0s,f1s,f0u,f1u,f0t,f1t
cf2py intent(out) ret
!      print *, "In the amplitude in Fortran"
!     print *, s
!      print *, t
!      print *, u
!      print *, param
      
      momega = dsqrt(s+t+u-3.d0*xmp**2)

      call f0f1(s,momega,f0s,f1s)
      call f0f1(u,momega,f0u,f1u)
      call f0f1(t,momega,f0t,f1t)
!      print *, "In the amplitude (after f0f1s) in Fortran"
 
      ret  = f0s+f0t+f0u+ param*(f1s + f1t + f1u) 
!      print *, f0s
!      print *, f0t
!      print *, f0u
!      print *, f1s
!      print *, f1t
!      print *, f1u
!      print *, ret
!      print *, AIMAG(ret)
      return
      end subroutine amp
      
      subroutine dummy(ret)
	  implicit none
	  integer :: idummy
	  real (8) :: ret
cf2py intent(out) ret
!      print *, "In the dummy function in Fortran"
      call uploadomega(idummy)
!      print *, "About to change ret"
      ret = 1.0
!	  ret = dble(idummy)
!      print *, "In the dummy function in Fortran"
	  return
	  end subroutine
	  

!     ---------------------------------
      module KTmodel
      complex (8), parameter :: xr=cmplx(1.d0,0.d0), xi=cmplx(0.d0,1.d0)
      integer, parameter     :: nintpl1 = 201, nomega = 36 !related to step and momegamin
      real (8), parameter    :: step = 0.010d0, momegamin = 0.6d0

      real (8), dimension (nintpl1) :: sn
      real (8), dimension (nintpl1,nomega) ::  storeref0, storebref0
      real (8), dimension (nintpl1,nomega) :: storecref0, storedref0
      real (8), dimension (nintpl1,nomega) ::  storeimf0, storebimf0
      real (8), dimension (nintpl1,nomega) :: storecimf0, storedimf0
      real (8), dimension (nintpl1,nomega) ::  storeref1, storebref1
      real (8), dimension (nintpl1,nomega) :: storecref1, storedref1
      real (8), dimension (nintpl1,nomega) ::  storeimf1, storebimf1
      real (8), dimension (nintpl1,nomega) :: storecimf1, storedimf1

      save sn
      save storeref0, storebref0, storecref0, storedref0
      save storeimf0, storebimf0, storecimf0, storedimf0
      save storeref1, storebref1, storecref1, storedref1
      save storeimf1, storebimf1, storecimf1, storedimf1
      end module KTmodel
!     ---------------------------------

      subroutine uploadomega(idummy)
      use KTmodel
      implicit none
      logical :: threebody
      character (40) :: genericname
      character (1)  :: namethreebody,numeric1,numeric2
      character (4)  :: extension
      character (47), dimension(100) :: filename ! 17=10+1+1+1+4; 100 (file names) related to i,j
      integer :: i,j,mwindex,ind,idummy
      
      real (8), dimension (nintpl1) :: ref0, bref0, cref0, dref0
      real (8), dimension (nintpl1) :: imf0, bimf0, cimf0, dimf0
      real (8), dimension (nintpl1) :: ref1, bref1, cref1, dref1
      real (8), dimension (nintpl1) :: imf1, bimf1, cimf1, dimf1
!     import
     

	  threebody = .true.

      genericname = '/mnt/home/mvick/PyPWA/XeonPhi/ListF_iter'
      if (threebody) then
         namethreebody = char(51) !51 -> 3
      else
         namethreebody = char(48) !48 -> 0
      endif
      extension = '.dat'
      ind = 0
      do i=0,9
         do j=0,9
            ind = ind + 1
            numeric1 = char(48+i)
            numeric2 = char(48+j)
            filename(ind) = genericname // namethreebody // numeric1 
     c           // numeric2 // extension
!            print *, "In the dummy function in Fortran"
!           print *, filename(ind)
         enddo
      enddo
!     print *, "In the dummy function in Fortran"

      do mwindex = 1,nomega
         open(1,file=filename(mwindex),status='old')
!     read import
         do i=1, nintpl1
            read(1,*) sn(i),ref0(i),imf0(i),ref1(i),imf1(i)
         enddo
         close(1)

         

!     interpolation (determination of the coefficients)
!      print *, "Before spline in Fortran"
         call spline(nintpl1,sn,ref0,bref0,cref0,dref0) 
!       print *, "In the spline function in Fortran"
         call spline(nintpl1,sn,imf0,bimf0,cimf0,dimf0) 
         call spline(nintpl1,sn,ref1,bref1,cref1,dref1) 
         call spline(nintpl1,sn,imf1,bimf1,cimf1,dimf1) 
         
         do i=1,nintpl1
!            print *, i
!           print *, nintpl1
            storeref0(i,mwindex)  =  ref0(i)
            storebref0(i,mwindex) = bref0(i)
            storecref0(i,mwindex) = cref0(i)
            storedref0(i,mwindex) = dref0(i)
            
            storeimf0(i,mwindex)  =  imf0(i)
            storebimf0(i,mwindex) = bimf0(i)
            storecimf0(i,mwindex) = cimf0(i)
            storedimf0(i,mwindex) = dimf0(i)
            
            storeref1(i,mwindex)  =  ref1(i)
            storebref1(i,mwindex) = bref1(i)
            storecref1(i,mwindex) = cref1(i)
            storedref1(i,mwindex) = dref1(i)
            
            storeimf1(i,mwindex)  =  imf1(i)
            storebimf1(i,mwindex) = bimf1(i)
            storecimf1(i,mwindex) = cimf1(i)
            storedimf1(i,mwindex) = dimf1(i)
         enddo
      enddo  
!      print *, "Declaring idummy"  
	  idummy = 1
      return
      end subroutine uploadomega
!     -----------------------------------------------------------------------
      subroutine f0f1(s,momega,f0,f1)
      use KTmodel
      implicit none
!     input
      real (8) :: s,momega
!     output
      complex (8) :: f0,f1
!     internal variables
      integer :: i,mwindex
      real (8), dimension (nintpl1) :: ref0, bref0, cref0, dref0
      real (8), dimension (nintpl1) :: imf0, bimf0, cimf0, dimf0
      real (8), dimension (nintpl1) :: ref1, bref1, cref1, dref1
      real (8), dimension (nintpl1) :: imf1, bimf1, cimf1, dimf1
      real (8) :: ref0sd,imf0sd,ref1sd,imf1sd
      real (8) :: ref0su,imf0su,ref1su,imf1su
      real (8) :: momegad,momegau
      complex (8) :: f0su,f0sd,f1su,f1sd
!     external functions
      real(8), external :: interpolate

      mwindex = 1+int((momega-momegamin)/step)
      momegad = momegamin + dble(mwindex-1)*step
      momegau = momegamin + dble(mwindex)*step

      do i=1,nintpl1
          ref0(i) =  storeref0(i,mwindex)  
         bref0(i) = storebref0(i,mwindex) 
         cref0(i) = storecref0(i,mwindex) 
         dref0(i) = storedref0(i,mwindex) 
         
          imf0(i) =  storeimf0(i,mwindex) 
         bimf0(i) = storebimf0(i,mwindex) 
         cimf0(i) = storecimf0(i,mwindex) 
         dimf0(i) = storedimf0(i,mwindex)
         
          ref1(i) =  storeref1(i,mwindex)  
         bref1(i) = storebref1(i,mwindex) 
         cref1(i) = storecref1(i,mwindex)
         dref1(i) = storedref1(i,mwindex)
          
          imf1(i) =  storeimf1(i,mwindex) 
         bimf1(i) = storebimf1(i,mwindex)
         cimf1(i) = storecimf1(i,mwindex) 
         dimf1(i) = storedimf1(i,mwindex)         
      enddo

      ref0sd = interpolate(nintpl1,s,sn,ref0,bref0,cref0,dref0)
      imf0sd = interpolate(nintpl1,s,sn,imf0,bimf0,cimf0,dimf0)
      ref1sd = interpolate(nintpl1,s,sn,ref1,bref1,cref1,dref1)
      imf1sd = interpolate(nintpl1,s,sn,imf1,bimf1,cimf1,dimf1)

      f0sd = ref0sd+xi*imf0sd
      f1sd = ref1sd+xi*imf1sd

      mwindex = mwindex + 1
      do i=1,nintpl1
          ref0(i) =  storeref0(i,mwindex)  
         bref0(i) = storebref0(i,mwindex) 
         cref0(i) = storecref0(i,mwindex) 
         dref0(i) = storedref0(i,mwindex) 
         
          imf0(i) =  storeimf0(i,mwindex) 
         bimf0(i) = storebimf0(i,mwindex) 
         cimf0(i) = storecimf0(i,mwindex) 
         dimf0(i) = storedimf0(i,mwindex)
         
          ref1(i) =  storeref1(i,mwindex)  
         bref1(i) = storebref1(i,mwindex) 
         cref1(i) = storecref1(i,mwindex)
         dref1(i) = storedref1(i,mwindex)
          
          imf1(i) =  storeimf1(i,mwindex) 
         bimf1(i) = storebimf1(i,mwindex)
         cimf1(i) = storecimf1(i,mwindex) 
         dimf1(i) = storedimf1(i,mwindex)         
      enddo

      ref0su = interpolate(nintpl1,s,sn,ref0,bref0,cref0,dref0)
      imf0su = interpolate(nintpl1,s,sn,imf0,bimf0,cimf0,dimf0)
      ref1su = interpolate(nintpl1,s,sn,ref1,bref1,cref1,dref1)
      imf1su = interpolate(nintpl1,s,sn,imf1,bimf1,cimf1,dimf1)

      f0su = ref0su+xi*imf0su
      f1su = ref1su+xi*imf1su

      f0 = (f0su-f0sd)*momega/step + (f0sd*momegau-f0su*momegad)/step
      f1 = (f1su-f1sd)*momega/step + (f1sd*momegau-f1su*momegad)/step

      return
      end subroutine f0f1
!     -----------------------------------------------------------------------
!     interpolation subroutine
!     -----------------------------------------------------------------------
      subroutine spline(n,x,y,b,c,d)
      implicit double precision (a-h,o-z)

      real (8) x(n),y(n),b(n),c(n),d(n)

      nm1 = n-1
      if(n.lt.2) return
      if(n.lt.3) goto 50

      d(1)=x(2)-x(1)
      c(2)=(y(2)-y(1))/d(1)
      do 10 i=2,nm1
         d(i)=x(i+1)-x(i)
         b(i)=2.0*(d(i-1)+d(i))
         c(i+1)=(y(i+1)-y(i))/d(i)
         c(i)=c(i+1)-c(i)
 10   continue
      
      b(1)=-d(1)
      b(n)=-d(n-1)
      c(1)=0.0
      c(n)=0.0
      if(n.eq.3) goto 15
      c(1)=c(3)/(x(4)-x(2))-c(2)/(x(3)-x(1))
      c(n)=c(n-1)/(x(n)-x(n-2))-c(n-2)/(x(n-1)-x(n-3))
      c(1)=c(1)*d(1)**2/(x(4)-x(1))
      c(n)=-c(n)*d(n-1)**2/(x(n)-x(n-3))
      
 15   do 20 i=2,n
         t=d(i-1)/b(i-1)
         b(i)=b(i)-t*d(i-1)
         c(i)=c(i)-t*c(i-1)
 20   continue
      
      c(n)=c(n)/b(n)
      do 30 ib=1,nm1
         i=n-ib
         c(i)=(c(i)-d(i)*c(i+1))/b(i)
 30   continue

      b(n)=(y(n)-y(nm1))/d(nm1)+d(nm1)*(c(nm1)+2.0*c(n))
      do 40 i=1,nm1
         b(i)=(y(i+1)-y(i))/d(i)-d(i)*(c(i+1)+2.0*c(i))
         d(i)=(c(i+1)-c(i))/d(i)
         c(i)=3.0*c(i)
 40   continue
      c(n)=3.0*c(n)
      d(n)=d(n-1)
      return
        
 50   b(1)=(y(2)-y(1))/(x(2)-x(1))
      c(1)=0.0
      d(1)=0.0
      b(2)=b(1)
      c(2)=0.0
      d(2)=0.0
      return
      end
      
      real (8) function interpolate(n,u,x,y,b,c,d)
     *     result (output)
      implicit double precision (a-h,o-z)
      real (8) x(n),y(n),b(n),c(n),d(n)
      data i /1/
      
      if(i.ge.n) i=1
      if(u.lt.x(i)) goto 10
      if(u.le.x(i+1)) goto 30
      
 10   i=1
      j=n+1
 20   k=(i+j)/2
      if(u.lt.x(k)) j=k
      if(u.ge.x(k)) i=k
      if(j.gt.i+1) goto 20
      
 30   dx=u-x(i)
      output=y(i)+dx*(b(i)+dx*(c(i)+dx*d(i)))
      return
      end
      
