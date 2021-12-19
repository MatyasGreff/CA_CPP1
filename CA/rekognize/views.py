from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponse
import logging
import boto3
from botocore.exceptions import ClientError
import os
from .models import Image
import secrets
import json
from CA.settings import AWS_STORAGE_BUCKET_NAME, AWS_S3_ACCESS_KEY_ID, AWS_S3_SECRET_ACCESS_KEY, BASE_DIR #S3 credentials imported from settings.py
import boto3.session #This is important, every request to S3 and rekognition will initiate a new session, so we don't get a token expired error after 15 minutes
from rekognition_jsonParser import rekognition_jsonParser #This is the library built by me



def index(request): #The index page, also serves as the object rekognition page
    return_img = ''
    rekog = ''
    names = ''
    if request.method == 'POST': #If a form is sent
        data = request.POST
        image_req = request.FILES.get('image') #Get the image file from the form response
        _, f_ext = os.path.splitext(image_req.name) 
        if f_ext not in ['.png', '.jpg', '.jpeg', '.JPG']: #Allowed file extensions
            names = 'Not allowed file extension'
        else:
            random_hex = secrets.token_hex(24) #Rename files, as they will all be stored in the same bucket, thus is an easy way to ensure there are no file name conflicts
            image_req.name = random_hex + f_ext #Rebuilding the filename + extension
            upload = Image.objects.create(  #Create a new object from the Image model
                image=image_req,
                )
            return_img = Image.objects.get(image=upload) #Getting the object that was just created
            rekog = obj_rekog(str(image_req.name)) #Passing the new image to the function below: obj_rekog, returns a 2D list of data
            if rekog:
                names = rekog.pop(0) #Pop out the first list of the 2D list that was returned from the function
                rekog = rekog[0] #Making the remaining 2D list a 1D list
            else:
                names = ['No objects identified']
            Image.objects.filter(id=return_img.id).update(description=names) #Adding rekognition result to the object
    context = {'return_img': return_img, 'rekog': rekog, 'names': names}
    return render(request, 'rekognize/index.html', context) #Returning variables to the template
    
    
    
def celebrity(request): #This view and is function below is very similar to the first one, only a few things differ so I will not make more comments
    return_img = ''
    rekog = ''
    names = ''
    if request.method == 'POST':
        print(BASE_DIR)
        data = request.POST
        image_req = request.FILES.get('image')
        _, f_ext = os.path.splitext(image_req.name)
        if f_ext not in ['.png', '.jpg', '.jpeg', '.JPG']:
            names = 'Not allowed file extension'
        else:
            random_hex = secrets.token_hex(24)
            image_req.name = random_hex + f_ext
            upload = Image.objects.create(
                image=image_req,
                )
            return_img = Image.objects.get(image=upload)
            rekog = test2(str(image_req.name))
            if rekog:
                names = rekog.pop(0)
                rekog = rekog[0]
            else:    
                names = ['No celebrities identified']
            Image.objects.filter(id=return_img.id).update(description=names)
    context = {'return_img': return_img, 'rekog': rekog, 'names': names}
    return render(request, 'rekognize/celebrity.html', context)
    

def about(request): #Static about page
    return render(request, 'rekognize/about.html')
    
    
def allimages(request): #Query the db and display all images from the S3 bucket, based on Id
    images = Image.objects.all()
    paginator = Paginator(Image.objects.all(), 4) #Pagination added, set to 4 images per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'images': images, 'page_obj': page_obj}
    return render(request, 'rekognize/allimages.html', context)
    
    
def viewimage(request, pk): #View added to view images in their original size 
    image = Image.objects.get(id=pk)
    return render(request, 'rekognize/viewimage.html', {'image': image})

    
def obj_rekog(image):
    my_session = boto3.session.Session() #New session must be created, I was getting expired token errors before this line was added
    client = my_session.client("rekognition", region_name="eu-west-1") #Initializing the rekognition service
    s3 = my_session.client('s3', aws_access_key_id=AWS_S3_ACCESS_KEY_ID, aws_secret_access_key=AWS_S3_SECRET_ACCESS_KEY) #New S3 session
    fileObj = s3.get_object(Bucket = AWS_STORAGE_BUCKET_NAME, Key=image) #When the new object was created from the Image model, it automatically uploaded it to the S3 bucket
    file_content = fileObj["Body"].read() 
    response = client.detect_labels(Image = {"S3Object": {"Bucket": AWS_STORAGE_BUCKET_NAME, "Name": image}}, MaxLabels=3, MinConfidence=70) 
    final_list = rekognition_jsonParser.detectLabel_jsonParser(response) #This is the rekognition_jsonParser library created for this project, takes the rekognition response and turns it into a 2D list
    return final_list #2D list created with the library is passed back to the index view
    
def test2(image):
    my_session = boto3.session.Session()
    client = my_session.client("rekognition", region_name="eu-west-1")
    s3 = my_session.client('s3', aws_access_key_id=AWS_S3_ACCESS_KEY_ID, aws_secret_access_key=AWS_S3_SECRET_ACCESS_KEY)
    fileObj = s3.get_object(Bucket = AWS_STORAGE_BUCKET_NAME, Key=image)
    file_content = fileObj["Body"].read()
    response = client.recognize_celebrities(Image = {"S3Object": {"Bucket": AWS_STORAGE_BUCKET_NAME, "Name": image}})
    final_list = rekognition_jsonParser.celebrity_jsonParser(response)
    return final_list
    
   
   
