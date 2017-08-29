import numpy as np
import os, sys, unittest, cv2, warnings

from datetime import datetime
from test.config import config
from pysmap.mltools.crowd_model import CrowdModel
from keras.applications.resnet50 import preprocess_input
# from matplotlib.testing.decorators import image_comparison

class TestCrowdModel(unittest.TestCase):
    def test_control(self):
        '''
        a control test to make sure everything
        in the unittest framework is working
        '''
        self.assertTrue(True)

    def test_model_loads_file(self):
        '''
        test that the model loads a model
        file properly and produces a model object
        '''
        cm = CrowdModel(config['crowd']['resnet50'], dl=False, talk=False)
        assert type(cm) is CrowdModel

    def test_model_dl_file(self):
        '''
        test that the model class can download a file
        from the server where we store model files
        '''
        cm = CrowdModel(config['crowd']['dl_path'], dl=True, talk=True)
        statinfo = os.stat(config['crowd']['dl_path'])
        assert os.path.exists(config['crowd']['dl_path'])
        assert statinfo.st_size == 295489952
        assert type(cm) is CrowdModel
        files = [config['crowd']['crowd_img'], config['crowd']['noncrowd_img']]
        preds = cm.predict_files(files)
        assert len(preds) > 0
        assert preds[0][0] > 0.9 # should be 0.997
        assert preds[1][0] < 0.1 # sould be 0.0034

    def test_model_predicts_imgs(self):
        '''
        test that a model can make predictions from
        an array of imgs that have already been loaded
        '''
        files = [config['crowd']['crowd_img'], config['crowd']['noncrowd_img']]
        imgs = np.zeros((len(files),224,224,3))
        for i, file in enumerate(files):
            img = cv2.imread(file).astype('float64')
            img = cv2.resize(img, (224,224))
            imgs[i] = img
        cm = CrowdModel(config['crowd']['resnet50'], dl=False, talk=False)
        preds = cm.predict_imgs(imgs)
        assert len(preds) > 0
        assert preds[0][0] > 0.9 # should be 0.997
        assert preds[1][0] < 0.1 # sould be 0.0034

    def test_model_predicts_files(self):
        '''
        test that the model class cna predict from image files
        this loads the images, prepocesses then predicts
        '''
        cm = CrowdModel(config['crowd']['resnet50'], dl=False, talk=False)
        files = [config['crowd']['crowd_img'], config['crowd']['noncrowd_img']]
        preds = cm.predict_files(files)
        assert len(preds) > 0
        assert preds[0][0] > 0.9 # should be 0.997
        assert preds[1][0] < 0.1 # sould be 0.00

    # @image_comparison(baseline_images=['test_view_preds'])
    # def test_view_preds(self):
    #     files = [config['crowd']['crowd_img'], config['crowd']['noncrowd_img']]
    #     imgs = np.zeros((len(files),224,224,3))
    #     for i, file in enumerate(files):
    #         img = cv2.imread(file).astype('float64')
    #         img = cv2.resize(img, (224,224))
    #         imgs[i] = img
    #     cm = CrowdModel(config['crowd']['resnet50'], dl=False, talk=False)
    #     preds = cm.predict_imgs(imgs)
    #     assert len(preds) > 0
    #     assert preds[0][0] > 0.9 # should be 0.997
    #     assert preds[1][0] < 0.1 # sould be 0.00
    #     view_predictions(imgs, preds, np.array([[1],[0]]), 0, 2)

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    unittest.main()
