# Simulation with Geant4

## 1. Enviroment
Set env with `cvmfs` setup.

```
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsenv
source /cvmfs/sft.cern.ch/lcg/views/geant-latest/x86_64-centos7-gcc7-opt/setup.sh
```


## 2. How to simulate
Compile with CMake.

```
mkdir build
cd build
cmake ..
make -j 4
```

When you get `generate` exe file in build folder, follow below command.

```
./generate ../macro/run_e+_50GeV.mac test.root
```

`run_e+_50GeV.mac` is just macro file to run simulation. You can use others by macro folder. `test.root` is output file name.
