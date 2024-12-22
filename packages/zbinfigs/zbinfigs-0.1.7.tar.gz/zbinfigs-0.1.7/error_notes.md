when running  
```bash
pip install -e .  
```
  
the path to the module was not correct and stopped at the parent directory, rather than directing to the source. This did not occur in a tiny test case.  
This was linked to specifying the hatchling target wheel as 'src'.