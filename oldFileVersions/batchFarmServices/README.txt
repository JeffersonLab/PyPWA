PythonPWA Batch Farm Documentation
===================================================

This document contains the name and a brief description of each program needed to run pythonPWA in the batch Farm.

*****pythonPWA and batchFarmServices require a /data directory and an /MC directory as well as program specific submission directories*****
*****all specified programs and directories need to be in the same top directory unless otherwise specified*****
*****pythonPWA and batchFarmServices requires the numpy and tkinter python modules; both are available on the i/batch farm.*****

dirSplitter.py: creates /MC/*_MeV and /data/*_MeV data structure
                1) follow the prompts


mkSETS.py: creates /data/*_MeV/set_i data structure
           1) follow the prompts


GUI_submit: A graphic user interface for submitting all, or specific mass bins for creating Monte-Carlo 3pi data. 
            1) choose a bin width and max number of events. then choose an i value in the command prompt for which "set" you're 
               submitting jobs for if you are splitting your mass bins.
            2) choose "ALL", or some bins to submit for.(Be sure to "print list" to check to make sure you chose the right bins.
            3) click "done" and then enter y or n into the command prompt to finish. 
            ***Requires "/subMCs"***
            ****Finished product will be saved to the /MC in the correct mass bin****


mvGAMP.py: moves all *_MeV.gamp MC files to your /data into the correct /set_i and renames them events.gamp.
           moves all output.gamp.index_i MC files to /data and into the correct /set_i and removes the _i tag


gamp_main.py: Submits GAMP jobs for all events.gamp files in /data to create .bamp files for the waves in your data.
              ***Requires /keyfiles, the keyfiles for included waves, and /subGamps***


ACCEPT.py: submits acceptanceFilter_farm.py jobs.
           1) follow the prompts
           ***requires /genACC***

>>>> acceptanceFilter_farm.py: creates events.pf files in the correct /data/*_MeV/set_i

>>>>>>>> events.pf is a text file where each line corresponds to an event in events.gamp. If the line is a 1 that event would be 
         "accepted" by the hallD
         detector. If it is a 0 it is discarded. 

alpha_main.py: submits AlphaGen.jar jobs.
               1) follow the prompts
               ***requires /genAlpha***

>>>> AlphaGen.jar: creates several .txt files, most importantly alphaevents.txt in the correct directory based on the prompts.


subPyNormInt.py: submits run_normintFarm.py jobs.
                 1) follow the prompts
                 ***requires /subPyNormInt***

>>>> run_normintFarm.py: creates normint.npy in the correct directory based on the prompts.

>>>>>>>> normint.npy is an array in numpy's .npy format. It is the normalization integral for the likelihood function. 


subCalcIlist.py: submits the calcIlistFarm.py job.
                 1) follow the prompts
                 ***requires /subILIST***
                 
>>>> calcIlistFarm.py: creates an iList.npy file in every /data/*_MeV/set_i.

>>>>>>>> iList.npy is an array in numpy's .npy format. It is the list of all calculated intensities for that set_i.


getIMaxList.py: gathers the maximum intensities from all iList.npy and creates IMaxList.npy in /data

>>>> IMaxList.npy is a numpy array of all maximum intensities. 


subpfFilter.py: submits pfFilterFarm.py jobs.
                1) follow the prompts
                ***requires /subpfFilter***

>>>> pfFilterFarm.py: creates accMC.gamp files in the correct /data/*_MeV/set_i 

>>>>>>>> accMC.gamp is the file of gamp events that passed the pf filter only. 


subdevTest.py: submits devTestFarm.py jobs.
               1) follow the prompts
               ***requires /subPyDEVS***

>>>> devTestFarm.py: creates selected_events.raw.gamp and selected_events.acc.gamp files in the correct /data/*_MeV/set_i based on the prompts.

>>>>>>>> selected_events.raw.gamp is the file of gamp events that passed the random/weight filter only.

>>>>>>>> selected_events.acc.gamp is the file of gamp events that passed the random/weight filter and the pf filter. 

MCdir.py: creates /data/*_MeV/data(mc)/acc(raw) file structure.
          1) follow the prompts
          2) run once choosing "data" and again choosing "mc"


cats.py: copies raw and filtered gamp files to their respective places /data/*_MeV/data(mc)/acc(raw) and renames them with the correct terminology and 
         concatenates all sets into large gamp files for each mass bin only.
         *events.gamp --> /mc/raw/rawMC.gamp*
         *accMC.gamp --> /mc/acc/accMC.gamp*
         *selected_events.raw.gamp --> /data/raw/rawDATA.gamp*
         *selected_events.acc.gamp --> /data/acc/accDATA.gamp*
         1) follow the prompts.    

Now you have to run alpha_main.py, gamp_main.py, and subPyNormInt.py again on the filtered and concatenated gamp files. 

    For all three, when it asks if you have run devTest choose 'y' and then answer whether or not you are runing them for mc, or data; acc, or raw.
    (you will not need normInts for data, so you won't be asked.) 








