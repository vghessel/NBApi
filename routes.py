from flask import Flask, request, jsonify
import sqlite3

app = Flask("main")

@app.route("/nba", methods=["GET"])
def teamInfo():

    adress = '/home/vinicius/NBA.db'
    conn = sqlite3.connect(adress)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute("SELECT * from NBAteams;")
    retorno = []
    for row in result.fetchall():
        item = {}
        item['id'] = row['id']
        item['team'] = row['team']
        item['conference'] = row['conference']
        item['founded'] = row['founded']
        item['titles'] = row['titles']
        item['goat'] = row['goat']
        retorno.append(item)

    return jsonify(retorno)

@app.route("/nba/ind")
def teamInd():

    body = request.get_json()

    adress = '/home/vinicius/NBA.db'
    conn = sqlite3.connect(adress)
    cur = conn.cursor()
    result = cur.execute("SELECT * from NBAteams WHERE id = '{0}';".format(body["id"]))

    return jsonify(result.fetchall())


@app.route("/nba/add", methods=["POST"])
def teamAdd():

    body = request.get_json()

    if("id" not in body):
        return geraResponse(400, "O parâmetro id é obrigatório!")
    if ("team" not in body):
        return geraResponse(400, "O parâmetro team é obrigatório!")
    if ("conference" not in body):
        return geraResponse(400, "O parâmetro conference é obrigatório!")
    if ("founded" not in body):
        return geraResponse(400, "O parâmetro founded é obrigatório!")
    if ("titles" not in body):
        return geraResponse(400, "O parâmetro titles é obrigatório!")
    if ("goat" not in body):
        return geraResponse(400, "O parâmetro goat é obrigatório!")

    adress = '/home/vinicius/NBA.db'
    conn = sqlite3.connect(adress)
    cur = conn.cursor()
    result = cur.execute("INSERT INTO NBAteams (id, team, conference, founded, titles, goat) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}');".format(body["id"], body["team"], body["conference"], body["founded"], body["titles"], body["goat"]))

    conn.commit()
    conn.close()

    return geraResponse(200, "Time criado", "time:", body["team"])

@app.route("/nba/update", methods=["PUT"])
def teamUpdate():

    adress = '/home/vinicius/NBA.db'
    conn = sqlite3.connect(adress)
    cur = conn.cursor()

    body = request.get_json()

    if ("id" not in body):
        return geraResponse(400, "O parâmetro id é obrigatório!")
    else:
        team = 'NULL'
        conference = 'NULL'
        founded = 'NULL'
        titles = 'NULL'
        goat = 'NULL'
        if ("team" in body):
            team = "'{}'".format(body["team"])
        if ("conference" in body):
            conference = "'{}'".format(body["conference"])
        if ("founded" in body):
            founded = "'{}'".format(body["founded"])
        if ("titles" in body):
            titles = "'{}'".format(body["titles"])
        if ("goat" in body):
            goat = "'{}'".format(body["goat"])

        result = cur.execute('''
        UPDATE
          NBAteams
        SET
          team = coalesce({0}, team), 
          conference = coalesce({1}, conference), 
          founded = coalesce({2}, founded), 
          titles = coalesce({3}, titles), 
          goat = coalesce({4}, goat)               
        WHERE id = '{5}';
        '''.format(team, conference, founded, titles, goat, body["id"]))

    conn.commit()
    conn.close()

    return geraResponse(200, "Time atualizado", "time:", body["team"])

@app.route("/nba/delete", methods=["DELETE"])
def teamDelete():

    body = request.get_json()

    if ("id" not in body):
        return geraResponse(400, "Informar apenas o parâmetro id")

    adress = '/home/vinicius/NBA.db'
    conn = sqlite3.connect(adress)
    cur = conn.cursor()
    result = cur.execute("DELETE from NBAteams WHERE id = '{0}';".format(body["id"]))

    conn.commit()
    conn.close()

    return geraResponse(200, "Time deletado", "id:", body["id"])

def geraResponse(status, mensagem, nome_do_conteudo=False, conteudo=False):
    response = {}
    response["status"] = status
    response["mensagem"] = mensagem

    if(nome_do_conteudo and conteudo):
        response[nome_do_conteudo] = conteudo

    return response

app.run()