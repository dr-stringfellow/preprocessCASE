for i in /data/t3home000/bmaier/CASE/BB_UL_MC_small/BB*h5; do echo $i; done | grep -v si | grep -v testset | xargs -n1 -P4 python3 cut_sideband_signal.py

