# Jupyter Notebooks
It's not always obvious how to make your virtual environment accessible in a Jupyter notebook. Below is a work in progress explaining how you can do so.  

## Setup (Rough guidelines; TBC)
* Create a virtual environment: e.g. `\path\to\v38\python.exe -m venv myenv`
* Activate your environment
* Install ipykernel: `pip install ipykernel`
* Install `python -m ipykernel install --name=myenv`
 
## Online Resources
* I used this guide: https://janakiev.com/blog/jupyter-virtual-envs/
    * I followed this but didn't use the `--user` option
* The Ipython Docs: https://ipython.readthedocs.io/en/latest/install/index.html

## Debugging:
* There is a bug when using Python 3.6.0. Try a more recent version.