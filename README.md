# Imager 
A simple to deploy image proxy — imager — that can resize images on demand.


The proxy will help to resize the image width and height, all images are stored on AWS-S3, a small cache system(on AWS-S3) is added with the 48 hours TTL(time to live).


# Resize any existing image of S3:

The proxy will help to resize any uploaded image on the S3 to resize it with any dimensions. Here is the API syntax and example:

```
 # Syntax:

 <Proxy-DNS/IP>/resize?width=<width>&height=<height>&path=<File path in S3>

 # Example

 imager.example.com/resize?width=500&height=500&path=somepic.png

 # Output

 https://imager.example.com/500x500/sompic.png
```

# To get the actual URL of the image:
To get the actual image of the resized image simply give the URL of the resized image and it will provide the actual URL.

```
 # Input

 https://imager.example.com/500x500/path/of/sompic.png

 # Output

 https://s3.ap-south-1.amazonaws.com/S3-bucket-name/path/of/sompic.png

```


# Build Imager on your local machine:

 1. Add AWS credentials in the `.env` file. (i.e. the Access key and Secret key)
 2. Update the following environment variables in the `docker-compose.yml`:
 ```
            - S3_BUCKET=<Bucket Name, e.g.;my-test.example.com>
            - S3_OBJECT_PREFIX=<e.g.; https://s3.ap-south-1.amazonaws.com/>
            - PROXY_HOST=<e.g. localhost/DNS>
            - CLOUDFRONT_ORIGIN=<e.g. https://data.example.com/loans/>
 ```
 3. Run `generate_certificates.sh` and generete self-signed certificate to enable SSH for service.
 4. Run below command to setup the imager on your machine:
 ```
  docker-compose up -d
 ```
 5. All resources can be destroyed using:
 ```
 docker compose down
 ```


# Prerequisites:
  1. docker should be installed.
  2. Cloudfront should be configured with custom origin, to pass all the requests from the Imager proxy. Here are the steps to set custom origin:
  https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/RequestAndResponseBehaviorCustomOrigin.html
