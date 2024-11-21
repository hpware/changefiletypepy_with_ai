# 轉換檔案成 PNG 的程式
## 安裝 Install
Linux 
```sh
git clone https://github.com/hpware/changefiletypepy
cd changefiletypepy
python3 createdir.py
python3 -m pip install -r requirements.txt
```
Windows (cmd)
```cmd
git clone https://github.com/hpware/changefiletypepy
cd changefiletypepy
python createdir.py
python -m pip install -r requirements.txt
```
## 運行 Execute
i 的資料夾都是檔案 請運行 ```main.py```

If the "i" folder is full of image files, then run ```main.py```

i 的資料夾都是資料夾 請運行 ```main-dir.py```

If the "i" folder is full of folders, then run ```main-dir.py```