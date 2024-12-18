import torch
from timm.models.maxxvit import TransformerBlock2d
from timm.models._efficientnet_blocks import UniversalInvertedResidual
from pytorch_ggd.GGD import DynamicGGD

class AsCAN2D(torch.nn.Module):
    def __init__(self, input_dim, embed_dim, spatial_dim):
        super().__init__()
        norm=lambda num_features,**kw:torch.nn.RMSNorm((num_features, spatial_dim, spatial_dim))
        C=lambda:UniversalInvertedResidual(embed_dim,embed_dim,act_layer=torch.nn.GELU,norm_layer=norm)
        T=lambda:TransformerBlock2d(embed_dim,embed_dim)
        self.layers=torch.nn.Sequential(
            torch.nn.Conv2d(input_dim,embed_dim,kernel_size=1),
            norm(embed_dim),
            torch.nn.GELU(),
            C(),C(),C(),T(),
            C(),C(),T(),T(),
            C(),T(),T(),T()
        )
    def forward(self,x):
        return self.layers(x)

class WaveletPooling2D(torch.nn.Module):
    def __init__(self, embed_dim, spatial_dim, wpt, num_levels):
        super().__init__()
        self.wpt = wpt
        self.num_levels = num_levels
        current_spatial_dim = spatial_dim
        self.projection_down = torch.nn.ModuleList()
        for i in range(num_levels):
            self.projection_down.append(torch.nn.Sequential(
                    torch.nn.Conv2d(embed_dim, embed_dim // 4, kernel_size=1, padding=0),
                    torch.nn.RMSNorm((embed_dim // 4, current_spatial_dim, current_spatial_dim))
                ))
            current_spatial_dim = current_spatial_dim // 2
    def forward(self, x):
        for i in range(self.num_levels):
            x = self.projection_down[i](x)
            x = self.wpt.analysis_one_level(x)
        return x

class TFTClassifier(torch.nn.Module):
    def __init__(self, config, wpt):
        super().__init__()
        self.wpt = wpt
        self.ascan = AsCAN2D(input_dim=config.channels*(4**config.J), embed_dim=config.embed_dim)
        self.pool = WaveletPooling2D(embed_dim=config.embed_dim, wpt=wpt, num_levels=(config.crop_size//(2**config.J))//4)
        self.classifier = torch.nn.Sequential(
            torch.nn.Conv2d(config.embed_dim, config.classifier_num_classes, kernel_size=1),
            torch.nn.Flatten()
        )
    def forward(self,x):
        x = self.wpt(x)
        x = self.ascan(x)
        x = self.pool(x)
        return self.classifier(x)