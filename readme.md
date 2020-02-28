# Demo


**Terminal 1**:
```bash
python3 -m http.server 8000 --bind 127.0.0.1 -d ./demo_server_files
```
For run test server.

**Terminal 2**:
```bash
python demo.py "http://localhost:8000/" | tee downloaded.list | xargs wget -q -P ./downloaded

# OR

echo "http://localhost:8000/" | python demo.py --urls - | tee downloaded.list | xargs wget -q -P ./downloaded

# OR

cat crawl.list
# Output:
# http://localhost:8000

python demo.py --urls crawl.list | tee downloaded.list | xargs wget -q -P ./downloaded
```

Explanation:

- `tee` for save new urls for future download, use for breakpoints and can be used for skip downloeded files.
- `xargs` run wget for each line from pipe
- `wget -q -P ./downloaded` for download url. `-q` for no output, `-P` for download files into `./downloaded` directory.
