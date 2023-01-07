# Generate cs class from json model

## example
```json
{
  "full_name": "quimby",
  "age": 45
}
```
generate class user_model.cs

```text
using UnityEngine;

[System.Serializable]
public class UserModel
{
	public string full_name; //example quimby 
	public int age; //example 45 
}
```

execute script
```bash
  python ./main.py --h
```
