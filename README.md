# microsuite - a collection of containers for MRI microstructural models

This repository has been created during [Brainhack Micro2Macro](https://brainhack-micro2macro.github.io), and includes several implementations of microstructural models that are ready-to-use. We use the [QMENTA SDK](https://docs.qmenta.com/sdk/) to:

* realize a shared template and API across different workflows;
* make containers that are ready-to-run on the QMENTA platform;
* make easy to define input and output.

The `test_sdk_tool.py` script from QMENTA included in this repository can be used to run locally the containers. Here is an example with the `amico` implementation of NODDI. First we build the image:

```
docker build -t amico-noddi AMICO-NODDI/
```

And then the workflow can be launched:

```
python test_sdk_tool.py amico-noddi ~/test_data ~/test_output/ --settings settings.json --values settings_values.json
```

To make the first tests, we used the [MICRA dataset](https://osf.io/z3mkn/).

### To-do list

* making all the containers following the same specifications;
* cover more workflows;
* prepare multiple versions of `settings_values.json` for testing on multiple shared datasets;

### Contributors
* Matteo Mancini
* Ricardo Rios - [RicardoRios46](https://github.com/RicardoRios46)


### References

Koller et al. (2021) "MICRA: Microstructural image compilation with repeated acquisitions", _NeuroImage_- [10.1016/j.neuroimage.2020.117406](https://doi.org/10.1016/j.neuroimage.2020.117406)

