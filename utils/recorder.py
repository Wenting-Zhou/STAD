import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import csv
import torchvision

class Recorder():
    def __init__(self, model, dataset, n, STNorm_n, TSNorm_n, st1, st2, attention, filename, n_layers, n_his, n_pred, model_name):
        super(Recorder, self).__init__()
        self.model = model
        self.STNorm_n = STNorm_n
        self.TSNorm_n = TSNorm_n
        self.st1 = st1
        self.st2 = st2
        self.attention = attention
        self.filename = filename
        self.n_layers = n_layers 
        self.n_his = n_his
        self.n_pred = n_pred
        self.model_name = model_name
    
    def pred_plot(self, real, pred, region, path = 'pic/'):
        np.save(path+ 'real_' + self.filename +'_'+ str(self.model_name) +'_' + str(self.STNorm_n) + '+' + str(self.TSNorm_n) + '_' + str(self.st1) + '+' + str(self.st2) + '_atten_' + str(self.attention) + '.npy', real)
        np.save(path + 'pred_' + self.filename +'_'+ str(self.model_name)+ '_'+ str(self.STNorm_n) + '+' + str(self.TSNorm_n) + '_' + str(self.st1) + '+' + str(self.st2)+ '_atten_' + str(self.attention) + '.npy', pred)
        for r in region:
          plt.rcParams['lines.linewidth'] = 1.1
          plt.figure(figsize=(8, 4), dpi = 200)
          plt.plot(range(int(real.shape[1] * 0.3)), real[0, 0:int(real.shape[1]  * 0.3), r, 0], label = 'real')
          plt.rcParams['lines.linewidth'] = 0.8
          for i in range(self.n_pred):
              plt.plot(range(i, int(real.shape[1] * 0.3) + i), pred[i, 0 : int(pred.shape[1] * 0.3), r, 0], label = str(i+1)+' step prediction')
          plt.legend()
          plt.savefig(path+ self.filename +'_'+ str(self.model_name) +'_region_' + str(r)+'_' + str(self.STNorm_n) + '+' + str(self.TSNorm_n) + '_' + str(self.st1) + '+' + str(self.st2) + 'atten' + str(self.attention) + '_in_one_plot.png')
          plt.close()
          
          
    def record_weights(self, attention_path =  'pic/'):
        S = nn.Softmax(dim = 0)
        file =open(attention_path + self.filename +'_'+ str(self.model_name) + '_' + str(self.STNorm_n) + '+' + str(self.TSNorm_n) + '_' + str(self.st1) + '+' + str(self.st2) +'.txt','a')
        file.write("="*20 + '\n')
        for i in range(self.STNorm_n + self.TSNorm_n):
            label = 'multiattention.0.single_attention_.' + str(i) + '.attention.attention_'
            para = self.model.state_dict()[label]
            para = para[:,0,0]
            _ = S(para)
            print(_)
            file.write(str(i+1))
            file.write('\n')
            file.write(f'&{_[0]:7.3}&{_[1]:7.3}&{_[2]:7.3}&{_[3]:7.3}\\' + '\n')
        file.close()
        
        
    def record_best_result(self, va, te, result_path = 'output/'):
        file =open(result_path + self.filename +'_'+ str(self.model_name) + '_'+ str(self.STNorm_n) + '+' + str(self.TSNorm_n) + '_' +str(self.st1)+ '_' + str(self.st2)+ '_atten_' + str(self.attention) +'.txt', 'a')
        file.write("="*20 + '\n')
        for i in range(self.n_pred):
            file.write(f'&MAPE & {va[i*3]*100:7.3}$\\%$& {te[i*3]:7.3}$\\%$&MAE & {va[i*3+1]:4.3f}& {te[i*3+1]:4.3f}&RMSE  &{va[i*3+2]:6.3f}&  {te[i*3+2]:6.3f}\\\\'+'\n')
        file.write(f'&{te[0]*100:7.3}$\\%$&{te[1]:7.3}&{te[2]:7.3}&{te[3]*100:7.3}$\\%$&{te[4]:7.3}&{te[5]:7.3}&{te[6]*100:7.3}$\\%$&{te[7]:7.3}&{te[8]:7.3}\\\\'+'\n')
        
                   
        file.close()
        
        
    def atten_plot(self, atten_, data_return, path = 'pic/', real_data_bool = True):
        pass
            
    def record_atten(self, atten_, data_return, path ='pic/', real_data_bool = True):
        np.save(path + 'atten' + self.filename +'_'+ str(self.model_name)+ '_'+ str(self.STNorm_n) +'+'+str(self.TSNorm_n)  +'_' + str(self.st1)+'_' +str(self.st2)+ '_atten' +'_'+ str(self.attention) + '.npy', atten_)
            

                   
