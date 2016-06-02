# -*- coding: utf-8 -*-
import os
from gluon.contrib import simplejson as json
from gluon import current
session = current.session

# XML config
XML_EXT = ['xml']
XML_FT = 'xml'
PRE_XML = "XML"
# De subida de XML
XML_DIR_NAME="xml"

# GPX config
GPX_EXT = ['gpx']
GPX_FT = 'gpx'
PRE_GPX = "GPX"
# De subida de GPX
GPX_DIR_NAME="gpx"

# Images config
IMAGES_EXT = ['jpg', 'png', 'gif']
IMAGES_FT = 'image'
PRE_IMAGE = "Image"
# De subida de fotos
IMAGES_DIR_NAME="images"
IMAGES_THUMB_DIR_NAME="thumbs"
IMAGES_OPTIM_DIR_NAME="optim"
IMAGES_THUMB_SIZE = (100, 100)
IMAGES_OPTIM_SIZE = (600, 400)

class qqFileUploader(object):

    def __init__(self, request, allowedExtensions=None, sizeLimit=None, uploadBasePath=None):
        self._request = request
        self.allowedExtensions = allowedExtensions or []
        self.sizeLimit = sizeLimit or 5120000
        self._fileType = None
        self._fileName = None
        self._fileExt = None
        self._curPath = None
        if uploadBasePath:
            self._uploadBasePath = uploadBasePath
        else:
            self._uploadBasePath = os.path.join(request.env.web2py_path,
                "applications", request.application, "uploads")
        self._gpxPath = os.path.join(self._uploadBasePath, GPX_DIR_NAME)
        self._xmlPath = os.path.join(self._uploadBasePath, XML_DIR_NAME)
        self._imagesPath= os.path.join(self._uploadBasePath, IMAGES_DIR_NAME)
        self._thumbsPath = os.path.join(self._imagesPath, IMAGES_THUMB_DIR_NAME)
        self._optimPath = os.path.join(self._imagesPath, IMAGES_OPTIM_DIR_NAME)
        # verify directory structure
        self.__checkDirectories()
        # By default, for images, create thumbs and optim
        self._createThumbs = True
        self._createOptim = True


    def __checkDirectories(self):
        """
        """
        #Check uploads dir
        self.__ensureDir(self._uploadBasePath)
        self.__ensureDir(self._imagesPath)
        self.__ensureDir(self._gpxPath)
        self.__ensureDir(self._xmlPath)
        self.__ensureDir(self._thumbsPath)
        self.__ensureDir(self._optimPath)


    def __ensureDir(self, dirPath):
        """
        """
        from os.path import exists
        from os import makedirs
        if not exists(dirPath):
            makedirs(dirPath)


    def setUploadDir(self, cDir):
        """
        """
        if cDir:
            self._uploadBasePath = cDir
            self.__ensureDir(self._uploadBasePath)


    def setImagesDir(self, cDir):
        """
        """
        if cDir:
            self._imagesPath= cDir
            self.__ensureDir(self._imagesPath)


    def setXmlDir(self, cDir):
        """
        """
        if cDir:
            self._xmlPath = cDir
            self.__ensureDir(self._xmlPath)


    def setGpxDir(self, cDir):
        """
        """
        if cDir:
            self._gpxPath = cDir
            self.__ensureDir(self._gpxPath)


    def setThumbsDir(self, cDir):
        """
        """
        if cDir:
            self._thumbsPath = cDir
            self.__ensureDir(self._thumbsPath)


    def setOptimDir(self, cDir):
        """
        """
        if cDir:
            self._optimPath = cDir
            self.__ensureDir(self._optimPath)


    def createThumbs(self, create):
        """
        """
        self._createThumbs = create


    def createOptim(self, create):
        """
        """
        self._createOptim = create


    def __getExtensionFromFileName(self, fileName):
        filename, extension = os.path.splitext(fileName)
        return extension.lower()


    def fileType(self):
        return self._fileType


    def __createThumbImage(self, tSize=IMAGES_THUMB_SIZE):
        from PIL import Image
        im = Image.open(self._filePath)
        if (im.size[0]>tSize[0]) or (im.size[1]>tSize[1]):
            im.thumbnail(tSize, Image.ANTIALIAS)
            thumbPath = os.path.join(self._thumbsPath, self._fileName)
            im.save(thumbPath)


    def __createOptimImage(self, oSize=IMAGES_OPTIM_SIZE):
        from PIL import Image
        im = Image.open(self._filePath)
        imAspect = float(im.size[0])/float(im.size[1])
        outAspect = float(oSize[0])/float(oSize[1])
        if imAspect >= outAspect:
            im.resize((oSize[0], int((float(oSize[0])/imAspect) + 0.5)), 3)
        else:
            im.resize((int((float(oSize[1])*imAspect) + 0.5), oSize[1]), 3)
        optimPath = os.path.join(self._optimPath, self._fileName)
        im.save(optimPath)


    def handleUpload(self):
        """
        """
        #read file info from stream
        #print request
        uploaded = self._request.body
        #get file size
        #fileSize = int(uploaded.im_self.META["CONTENT_LENGTH"])
        #get file name
        #fileName = request.environ["HTTP_X_FILE_NAME"]
        fn = self._request.wsgi.environ["HTTP_X_FILE_NAME"]
        fn = fn.strip()
        fn = fn.replace("%20", "_")
        splittedFN = fn.split(".")
        newFN = ''
        for i in range(0, len(splittedFN) - 1):
            newFN += splittedFN[i]
        newFE = splittedFN[len(splittedFN) - 1].lower()
        pre = ''
        if newFE in IMAGES_EXT:
            pre = PRE_IMAGE
            self._fileType = IMAGES_FT
            self._curPath = self._imagesPath
        elif newFE in XML_EXT:
            pre = PRE_XML
            self._fileType = XML_FT
            self._curPath = self._xmlPath
        elif newFE in GPX_EXT:
            pre = PRE_GPX
            self._fileType = GPX_FT
            self._curPath = self._gpxPath
        else:
            self._fileType = None
        import datetime
        timeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        self._fileName = "%s.%s_%s.%s" % (pre, newFN, timeStamp, newFE)
        self._fileExt = newFE
        self._filePath = os.path.join(self._curPath, self._fileName)
        #Set session variable
        session.uploadFile = self._fileName
        #check first for allowed file extensions
        #read the file content, if it is not read when the request is multi part then the client get an error
        if self.__getExtensionFromFileName(self._fileName) in self.allowedExtensions or ".*" in self.allowedExtensions:
            self.__ensureDir(self._curPath)
            #upload file
            fileContent = uploaded.read()
            #write file
            file = open(self._filePath, "wb+")
            file.write(fileContent)
            file.close()
            # If image create ...
            if self._fileType==IMAGES_FT:
                #Create thumb
                if self._createThumbs:
                    self.__createThumbImage()
                #Create optim
                if self._createOptim:
                    self.__createOptimImage()
            else:
                pass
            return json.dumps(
                {
                    "success": True,
                    'fileName': self._fileName
                }
            )
        else:
            return json.dumps(
                {
                    "error": "El archivo no tiene una extensión aceptada"
                }
            )
