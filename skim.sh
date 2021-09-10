for i in /eos/cms/store/group/phys_b2g/CASE/h5_files/full_run2/BB_UL_MC_small/BB*h5; do echo $i; done | grep -v si | grep -v testset | xargs -n1 -P4 -i python3 cut_sideband_signal.py {} /eos/cms/store/user/bmaier/cms/case/samples/ul/

