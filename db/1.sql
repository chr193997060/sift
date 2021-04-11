SELECT path
FROM img_path_md5 
WHERE img_md5 IN 
(SELECT img_md5 FROM img_tag WHERE tag2=4)
ORDER BY path
