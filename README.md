### Mock API Server
Create your own mock server with API documentation services such as Swagger.

##### Currently supports
- Swagger

##### Requirements
- Python 3.x
- pip (based on Python 3.x)

##### Steps to use
1. Clone the repository.
2. `cd` to your project.
3. [You may skip this step] Create virtual environment.
4. Install required libraries using `pip install -r requirements.txt`
4. Download your `swagger.json` file from Swagger UI.
5. Use the following to serve your file `python app.py -s /path/to/swagger.json`
##### Extended use
```
usage: app.py [-h] -s SOURCE [-p PORT] [-t {swagger}] [-sc STATUS_CODE] [-r RANDOM_SEED] [-d DEFAULT_VALUE [DEFAULT_VALUE ...]]
              [-l LIST_SIZE [LIST_SIZE ...]]

Options for mock responses

Required and optional arguments:
  -h, --help            show this help message and exit

  -s SOURCE, --source SOURCE
                        (Required) API reference source file path.
  
  -p PORT, --port PORT  (Optional,default=5000) Port number the app runs on.

  -t {swagger}, --type {swagger}
                        (Optional,default='swagger') Type of API reference. Currently only supports Swagger.

  -sc STATUS_CODE, --status_code STATUS_CODE
                        (Optional,default=200) Generates responses with status code provided.

  -r RANDOM_SEED, --random_seed RANDOM_SEED
                        (Optional) Generates random responses based on seed value.

  -d DEFAULT_VALUE [DEFAULT_VALUE ...], --default_value DEFAULT_VALUE [DEFAULT_VALUE ...]
                        (Optional) Sets default values in response body. Format key=value.

  -l LIST_SIZE [LIST_SIZE ...], --list_size LIST_SIZE [LIST_SIZE ...]
                        (Optional,default=[2]) Sets default size of list in response body.

```

If you would like to donate or know more contact: `bikcrum@gmail.com`

Thank you! Happy coding!