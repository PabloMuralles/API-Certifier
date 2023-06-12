import base64
import io
import qrcode

f = open('C:\\Users\Pablo\Desktop\GFG.html', 'w')

qr = qrcode.make('https://felpub.c.sat.gob.gt')

buffer = io.BytesIO()

qr.save(buffer, format="PNG")

img_str = base64.b64encode(buffer.getvalue()).decode('ascii')


html_template = """<html>
<head>
<title>Title</title>
</head>
<body>
<h2>Welcome To GFG</h2>
  
<p>Default code has been loaded into the Editor.</p>

<div><img src="data:image/png;base64{}"><div>

<p>{}</p>
  
</body>
</html>
""".format(img_str,img_str)
  
# writing the code into the file
f.write(html_template)
  
# close the file
f.close()