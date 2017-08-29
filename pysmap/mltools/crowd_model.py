import numpy as np
import gc, abc, cv2, requests, os, shutil, gzip

from pysmap.mltools.smapp_model import SmappModel
from keras.models import load_model
from keras.applications.resnet50 import preprocess_input

def download_file(url, local_url):
    r = requests.get(url, stream=True)
    with open(local_url, 'wb') as f:
        shutil.copyfileobj(r.raw, f)

def unzip_file(local_url, model_path):
    with gzip.open(local_url, 'rb') as fin:
        with open(model_path, 'wb') as fout:
            shutil.copyfileobj(fin, fout)

class CrowdModel(SmappModel):
    __metaclass__ = abc.ABCMeta

    def __init__(self, model_path, model_dl='http://165.227.83.131:82/', dl=True, talk=True):
        if dl or not os.path.exists(model_path):
            url = os.path.join(model_dl,'crowdv1.h5.gz')
            local_url = os.path.join('/'.join(model_path.split('/')[:-1]),'crowdv1.h5.gz')
            if talk: print('downloading model file to: {}'.format(local_url))
            download_file(url, local_url)
            unzip_file(local_url, model_path)
            if talk: print('downloaded model file to: {}'.format(model_path))
        if talk: print('loading model from from: {}'.format(model_path))
        self.model = load_model(model_path)

    def predict_imgs(self, imgs):
        '''
        takes an image input and predicts on it
        this expects an ndarray (heightxwidthxchannels)
        this model shouldbe a (Nx224x224x3) numpy array
        this method it noce if you want to do preprocessing
        then predict results on those preprocessed images
        this function expects the image array to be jpg
        '''
        imgs = preprocess_input(imgs)
        return self.model.predict(imgs)

    def predict_files(self, files):
        '''
        reads files off disk, resizes them
        and then predicts them, files should
        be a list or itrerable of file paths
        that lead to images, they are then
        loaded with opencv, resized, and predicted
        '''
        imgs = [0]*len(files)
        for i, file in enumerate(files):
            img = cv2.imread(file).astype('float64')
            img = cv2.resize(img, (224,224))
            img = preprocess_input(img)
            if img is None:
                print('failed to open: {}, continuing...'.format(file))
            imgs[i] = img
        return self.model.predict(np.array(imgs))

    def view_predictions(imgs, y_pred, y_true, start, end):
        '''
        displays the images in a grid formation from the 
        start index to the end index, y_true are the true
        labels for the images, y_pred should be your predictions
        imgs should be an (NxWxHx3) array of your input images

        '''
        fig, ax = plt.subplots(16, 4, sharex='col', sharey='row', figsize=(25, 100))
        for i, img in enumerate(imgs[start:end]):
            pred_label = y_pred[start:end][i]
            actual_label = y_true[i]
            ax[i//4][i%4].imshow(img)
            ax[i//4][i%4].annotate(pred_label[0],
                          (0,0), (0, -32), xycoords='axes fraction', 
                           textcoords='offset points', va='top', size=20)
            ax[i//4][i%4].annotate(actual_label,
                          (0,0), (200, -32), xycoords='axes fraction', 
                           textcoords='offset points', va='top', size=20)
            ax[i//4][i%4].axis('off')
        return ax
