from flask import jsonify, abort


#helper functions
def matchfield(req, record):
    def assignlmb(fi, v):
        record[fi] = v
        return fi
    updated = [assignlmb(fi, req[fi]) for fi in req.keys()]
    
    return updated

def tag_one(entity, fields, rec):
    if not rec:
        return(jsonify({"error":"404", "message":"no record found"}), 404)

    response = jsonify({entity: dict(zip(fields, rec))})
    return(response, 200)

def tag_many(entity, fields, recs, message="record not found"):
    if len(recs) == 0:
        return (jsonify({"error":"404", "message":message}),404)

    response = jsonify({entity:[dict(zip(fields, x)) for x in recs]})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return(response, 200)

queryify = lambda x:{True: "'{0}'".format(x), False:str(x)}[type(x)==str]
qiy = lambda x:"{0} = {1}".format(str.lower(x[0]), queryify(x[1]))
