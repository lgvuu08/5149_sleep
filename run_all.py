import io, json, sys, contextlib, warnings, logging, os, traceback
warnings.filterwarnings('ignore')
logging.disable(logging.CRITICAL)
os.environ['TQDM_DISABLE'] = '1'
sys.path.insert(0, os.path.dirname(__file__))
from snippets import CODE

out = {}
for k, code in CODE.items():
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            exec(compile(code, k, 'exec'), {'__name__': '__main__'})
        out[k] = buf.getvalue().rstrip()
    except Exception:
        out[k] = 'ERROR\n' + traceback.format_exc()
json.dump(out, open(os.path.join(os.path.dirname(__file__), 'outputs.json'), 'w'), indent=1)
for k, v in out.items():
    print('=' * 8, k); print(v)
