from __future__ import print_function, absolute_import, division

import json
import traceback
from cStringIO import StringIO
from pprint import pformat

from flask import Flask, render_template, Response, request

from toolz import first
from toolz.compatibility import map, zip

from multipledispatch import dispatch
from blaze import Data, compute, join, by, transform


app = Flask(__name__)


def jsonify(data, status=200, **kwargs):
    return Response(response=json.dumps(data), status=status,
                    **kwargs)


def strtypes(dshape):
    return map(str, dshape.measure.types)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data/<table>', methods=['GET'])
@app.route('/data/<table>/<int:n>', methods=['GET'])
def table(table, n=10):
    return compute(getattr(db, table)).head(n)


@app.route('/data/tables', methods=['GET'])
def tables():
    fields = db.fields
    dshapes = map(lambda field: getattr(db, field).dshape, fields)
    result = [dict(name=field,
                   dshape=dict(pairs=list(map(list, zip(dshape.measure.names,
                                                        strtypes(dshape))))))
              for field, dshape in zip(fields, dshapes)]
    return jsonify(result)


def get_command(r):
    data = json.loads(request.data)

    # why is this necessary?
    params = data['params']
    if not params:
        return ''
    return first(params)


@dispatch((dict, list, tuple))
def pprint(x):
    return pformat(x)


@dispatch(object)
def pprint(x):
    return repr(x)


def get_traceback():
    sio = StringIO()
    traceback.print_exc(file=sio)
    return sio.getvalue()


@app.route('/compute', methods=['POST'])
def compute_from_json():
    cmd = get_command(request)
    if not cmd:
        result = cmd
    else:
        try:
            # this might be the most insecure way to do this. ever.
            result = pprint(eval(cmd, {
                            'db': db,
                            'join': join,
                            'by': by,
                            'transform': transform
                            }))
        except Exception:
            result = get_traceback()
    return jsonify({'output': result})


if __name__ == '__main__':
    db = Data('blaze://localhost:6363')
    app.run(debug=True, port=23532)
