(import [flask [Blueprint jsonify]])
(import [checkit.apiUtils [*]])
(import [checkit.db [get_db]])

(setv bp (Blueprint "apiforms" __name__ :url_prefix "/api/v1.0/forms"))

(with-decorator (bp.route "/<string:name>" :methods ["GET"])
	(defn get_form [name]
		(jsonify {"form" {"schema" "hi"}})))
