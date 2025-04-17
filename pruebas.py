from tasks.classification import classify_image
import base64

with open("images/img5.jpg", "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

result = classify_image(b64)
print(result)
