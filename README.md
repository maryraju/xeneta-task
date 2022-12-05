# Xeneta Operations Task

## Task 1:

### Prerequistes
* AWS account and a user with acess to the below policies:
```
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "autoscaling:*",
        "codedeploy:*",
        "ec2:*",
        "lambda:*",
        "ecs:*",
        "elasticloadbalancing:*",
        "iam:AddRoleToInstanceProfile",
        "iam:AttachRolePolicy",
        "iam:CreateInstanceProfile",
        "iam:CreateRole",
        "iam:DeleteInstanceProfile",
        "iam:DeleteRole",
        "iam:DeleteRolePolicy",
        "iam:GetInstanceProfile",
        "iam:GetRole",
        "iam:GetRolePolicy",
        "iam:ListInstanceProfilesForRole",
        "iam:ListRolePolicies",
        "iam:ListRoles",
        "iam:PutRolePolicy",
        "iam:RemoveRoleFromInstanceProfile",
        "s3:*",
        "ssm:*",
		"cloudformation:*"
      ],
      "Resource": "*"
    }    

```
To create a user: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#Using_CreateUser_console

* AWS CLI(Optional)
The development environment resources are created in AWS. Hence aws cli is prefered. If not installed, you can use aws console.

### Steps to automate the development environment

* Go to task1 folder and open the file 'codedeploy_template.yaml'. 

The file contains the cloudformation template to automate the allocation of an ec2 instance and use code deploy to copy files from github to the ec2 server.

The parameter section of template is populated with values of resources existing in my aws account. If you have any of the resources change it accordingly.
If none of the resources are present, create the resources with the help of the doc:
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/create-key-pairs.html
https://docs.aws.amazon.com/codebuild/latest/userguide/cloudformation-vpc-template.html

* Move the 'codedeploy_template.yaml' from the folder and keep it in the local system and upload the remaining folders to git. Make sure 'appspec.yml' file is in the outside.

* Note down the git commit id and repository name. Edit the 'codedeploy_template.yaml' and give those values to 'Commit' and 'Repo' parameter default values.

* If code deployment from git is done for the first time, follow the instruction in the aws doc: https://docs.aws.amazon.com/codedeploy/latest/userguide/integrations-partners-github.html

![image](https://user-images.githubusercontent.com/74228590/205670671-7ec0e80e-6824-443d-9004-f6b0879384d4.png)

Click connect to Github and give your credentials and connect to github.

* Now run the below command in aws cli to create a cloudformation stack.

```
aws cloudformation package --template "<path to cloudformationtemplate>\codedeploy_template.yaml" --s3-bucket mybucket --output-template-file "<path to cloudformationtemplate>\packaged-template.yaml"

aws cloudformation deploy --template-file "<path to cloudformationtemplate>\packaged-template.yaml" --stack-name <stackname>  --capabilities CAPABILITY_NAMED_IAM
```

                                      OR
									  
* Go to AWS cloudformation console and click create stack. Upload the template.
Once completed will get successfully created/updated stack message

* Now go to EC2 services, select the gunicorn_app instance and connect to it.

* Navigate to /opt folder
```
 cd /opt
```

* Check if our folder is present there. 

* Change the folder permissions.

```
sudo chown ec2-user:ec2-user db/
sudo chown ec2-user:ec2-user db/*
sudo chown ec2-user:ec2-user rates/
sudo chown ec2-user:ec2-user rates/*
```

Here ec2-user is the username. If your username is different, use it instead of ec2-user.

* Change the 'dockerexec_script.sh' permissions.
```
sudo chown ec2-user:ec2-user dockerexec_script.sh
sudo chmod 777 dockerexec_script.sh
```

* Run the script.
```
./dockerexec_script.sh
```
This will create two docker containers with the API and db.

* Test the application
Get average rates between ports:
```
curl "http://127.0.0.1:3000/rates?date_from=2021-01-01&date_to=2021-01-31&orig_code=CNGGZ&dest_code=EETLL"
```

The output should be something like this:
```
{
   "rates" : [
      {
         "count" : 3,
         "day" : "2021-01-31",
         "price" : 1154.33333333333
      },
      {
         "count" : 3,
         "day" : "2021-01-30",
         "price" : 1154.33333333333
      },
      ...
   ]
}
```

### Troubleshooting

* Cloudformation stack creation issues.

Please check your iam roles. Verify if you have correct acess to create Iam roles, ec2 instances and to do codedeploy services.

Verify if the template is correct. Check for any errors in template. Also use disable rollback option. So that we can check the failure reason of the failed resource by directly going into that service.
```
aws cloudformation create-stack --stack-name myteststack --template-body file://DOC-EXAMPLE-BUCKET.json -–disable-rollback 
```
After inspection delete the stack.

* Application issues.

If you see the below error while executing the script

                OR
				
'500 Internal Server error' while fetching data, do the following.


Exec into my-postgresdb-container container.

```
docker exec -it my-postgresdb-container bash
```

Inside bash, execute the below command
```
psql -h localhost -U postgres < rates.sql
```

Now stop the my_gunicorn_app container
```
docker stop <containerid>
```

Start it agin.
```
docker start <containerid>
```

## Task 2:

The word doc contains the detailed answers of the second task.