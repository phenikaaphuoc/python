import torch
import torch.nn as nn
import torchvision

class Conv(nn.Module):
    def __init__(self,in_channels,out_channels,k,s,p,bias = False):
        super().__init__()

        self.main = nn.Sequential(
            nn.Conv2d(in_channels,out_channels,kernel_size=(k,k),stride=s,padding=p,bias = bias),
            nn.BatchNorm2d(out_channels),
            nn.SiLU(),
        )
    def forward(self,x):

        return self.main(x)
class SPPF(nn.Module):
    def __init__(self,in_channels,k_size = 5):
        super().__init__()

        self.conv1 = Conv(in_channels,in_channels,1,1,0)

        self.max1 = nn.MaxPool2d(k_size,stride=1,padding=k_size//2)
        self.max2 = nn.MaxPool2d(k_size, stride=1, padding=k_size // 2)
        self.max3 = nn.MaxPool2d(k_size, stride=1, padding=k_size // 2)

        self.conv2 = Conv(in_channels*4,in_channels,1,1,0)
    def forward(self,x):

        x1 = self.conv1(x)

        x2 = self.max1(x1)
        x3 = self.max2(x2)
        x4 = self.max3(x3)

        return self.conv2(torch.cat([x1,x2,x3,x4],dim=1))
class BottleNeck(nn.Module):
    def __init__(self,in_channels,shortcut ):
        super().__init__()

        self.shortcut = shortcut
        self.conv = nn.Sequential(
            Conv(in_channels,in_channels,3,1,1),
            Conv(in_channels,in_channels,3,1,1)
        )

    def forward(self,x):

        x1 = self.conv(x)
        if self.shortcut:
            x1  = x1 + x

        return x1
class C2f(nn.Module):

    def __init__(self,in_channels,out_channels,n,shortcut):
        super().__init__()

        self.conv1 = Conv(in_channels,out_channels,1,1,0)

        self.bottelnecks = nn.ModuleList()

        for _ in range(n):

            self.bottelnecks.append(BottleNeck(out_channels//2,shortcut))

        assert (out_channels%2==0)

        in_channels = out_channels//2*(n+2)

        self.conv2 = Conv(in_channels,out_channels,1,1,0)

        self.split = out_channels//2

    def forward(self,x):

        x = self.conv1(x)

        out ,input = x[:,:self.split],x[:,self.split:]

        shortcuts = [out,input]

        for bottleneck in self.bottelnecks:

            out = bottleneck(input)
            shortcuts.append(out)
            input = out

        x = torch.cat(shortcuts,dim=1)

        return self.conv2(x)
class BackBone(nn.Module):
    def __init__(self,in_chanels = 3,w = 1,r = 1,d = 1):
        super().__init__()
        n_shortcuts = int(d*3)

        self.feature_extractions = nn.ModuleList(
            [
                Conv(in_chanels,64,3,2,1),



                nn.Sequential(
                    Conv(64, 128, 3, 2, 1),
                    C2f(128,128,n_shortcuts,True),

                ),

                nn.Sequential(
                    Conv(128, 256, 3, 2, 1),
                    C2f(256,256,n_shortcuts*2,shortcut=True),

                ),

                nn.Sequential(
                    Conv(256, 512, 3, 2, 1),
                    C2f(512,512,n_shortcuts*2,shortcut=True),


                ),

                nn.Sequential(
                    Conv(512, 512, 3, 2, 1),
                    C2f(512,512,n_shortcuts,True),
                    SPPF(512)

                )

            ]
        )
    def forward(self,x):

        outputs = []
        input = x

        for feature_extraction in self.feature_extractions:

            outputs.append(feature_extraction(input))
            input = outputs[-1]
        return outputs
class Concat(nn.Module):
    def __init__(self,dim = 1):
        super().__init__()
        self.dim = dim
    def forward(self,x):

        return torch.cat(x,self.dim)
class Header(nn.Module):
    def __init__(self,n_c2f):
        super().__init__()

        self.main = [
            nn.ModuleList(
                [
                    nn.Upsample(None,scale_factor=2,mode = "nearest"),
                    Concat(dim=1),
                    C2f(1024,512,n_c2f,shortcut=False)
                ]
            ),
            nn.ModuleList(
                [
                    nn.Upsample(None, scale_factor=2, mode="nearest"),
                    Concat(dim=1),
                    C2f(768, 256, n_c2f, shortcut=False)
                ]
            )
        ]

        self.after = [
            nn.ModuleList(
                [
                    Conv(256,256,3,2,1),
                    Concat(dim=1),
                    C2f(768,512,n_c2f,shortcut=False)
                ]
            ),
            nn.ModuleList(
                [
                    Conv(512,512,3,2,1),
                    Concat(dim=1),
                    C2f(1024,512,n_c2f,shortcut=False)
                ]
            )
        ]
    def forward(self,inputs):

        inputs = inputs[::-1]
        outputs = [inputs[0]]

        for i,module in enumerate(self.main):

            output = module[0](outputs[-1])

            output = module[1]([inputs[i+1],output])
            output = module[2](output)

            outputs.append(output)

        inputs = outputs[::-1]
        outputs = [inputs[0]]

        for i, module in enumerate(self.after):
            output = module[0](outputs[-1])

            output = module[1]([inputs[i + 1], output])
            output = module[2](output)

            outputs.append(output)


        return outputs
    
class DFL(nn.Module):

    def __init__(self, c1=16):
        super().__init__()
        self.conv = nn.Conv2d(c1, 1, 1, bias=False).requires_grad_(False)
        x = torch.arange(c1, dtype=torch.float)
        self.conv.weight.data[:] = nn.Parameter(x.view(1, c1, 1, 1))
        self.c1 = c1

    def forward(self, x):
        b, c, a = x.shape  # batch, channels, anchors
        return self.conv(x.view(b, 4, self.c1, a).transpose(2, 1).softmax(1)).view(b, 4, a)
        # return self.conv(x.view(b, self.c1, 4, a).softmax(1)).view(b, 4, a)
class Detect(nn.Module):
    def __init__(self,channels = (256,512,512),n_c = 80,reg_max = 16):
        super().__init__()

        self.c = 4*reg_max
        self.n_c = n_c

        self.sequence1 =nn.ModuleList(
            [
                nn.Sequential(
                    Conv(c,c,3,1,1),
                    Conv(c,c,3,1,1),
                    nn.Conv2d(c,self.c,(1,1),1,0)
                )
                for c in channels
            ]
        )

        self.sequence2 = nn.ModuleList(
            [
                nn.Sequential(
                    Conv(c, c, 3, 1, 1),
                    Conv(c, c, 3, 1, 1),
                    nn.Conv2d(c, self.n_c+1, (1, 1), 1, 0)
                )
                for c in channels
            ]
        )
    def forward(self,x):
        assert (len(x)== 3)
        for i,input in enumerate(x):
            x[i] = (self.sequence1[i](input),self.sequence2[i](input))
        return x


backbone = BackBone()
x = torch.randn(1,3,640,640)
outputs = backbone(x)
head = Header(3)
outputs = head(outputs)
detect = Detect()

for out in  detect(outputs):
    print(out[0].shape)
    print(out[1].shape)
