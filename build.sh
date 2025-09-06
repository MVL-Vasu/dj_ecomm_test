echo "BUILD START"

python3 -m pip install -r requirements.txt
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput --clear

# 👇 Add this to debug what files are in staticfiles
echo "---- STATICFILES CONTENT ----"
ls -R staticfiles

echo "BUILD END"
