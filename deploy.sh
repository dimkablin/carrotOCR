echo "Check master branch"
git checkout master

echo "Push app..."
git push

echo "Deploying files to server..."
ssh -i ~/.ssh/id_rsa root@213.171.5.243 'cd ocr/releaseV3/carrotOCR/ && git checkout master && git pull'

echo "Done!"