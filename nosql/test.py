from FanGraph import FanGraph
import json
import pandas as pd
from py2neo import data, Graph, Node, NodeMatcher, Relationship, RelationshipMatcher

pd.set_option('display.width', 132)

fg = FanGraph()
print(fg)
def test1():
    q = 'MATCH (n:Person {born: {ln}}) RETURN n '
    r = fg.run_q(q, {"ln":1964})
    print('Result = ', r)
    if r is not None:
        d = r.data()
        print(d)


def test2():
    q = 'MATCH (p:Person {born: {ln}})-[r:ACTED_IN]->(n) RETURN p,r,n '
    r = fg.run_q(q, {"ln":1964})
    print('Result = ', r)
    if r is not None:
        d = r.data()
        print(json.dumps(d, indent=2))


def test3():

    tx = fg._graph.begin(autocommit=False)
    n = Node("Pet", name='Gus', kind="Cat")
    tx.create(n)
    tx.commit()


def test4():
    tx = fg._graph.begin(autocommit=False)
    try:
        tmp = {'label':'Pet', 'template':{'name':'Gus'}}
        r = fg.find_nodes_by_template(tmp)
        print('Pet=', r)
        tx.commit()
    except Exception as e:
        tx.rollback()

def test5():
    # test create comment and get comment
    tx = fg._graph.begin(autocommit=False)
    try:
        tmp = {'label':'Comment', 'template':{'comment':'good'}}
        fg.create_comment(uni='js1', comment='good', team_id='BOS')
        q = 'match (n:Team)<-[r:COMMENT_ON]-(c:Comment)-[x:COMMENT_BY]->(m:Fan)return n,r,c,x,m'
        r = fg.run_q(q,{})
        print('Comment:', json.dumps(r.data(), indent=2))
        r2 = fg.get_comment(comment_id='333e52e9-e9ca-49f1-bce4-a03294dcf133')
        print('Get comment:',r2)
    except Exception as e:
        tx.rollback()

def test6():
    # test create sub comment and get sub comment
    tx = fg._graph.begin(autocommit=False)
    try:
        tmp = {'label': 'Sub_comment', 'template': {'sub_comment': 'agree'}}
        fg.create_sub_comment(uni='dff9009999', origin_comment_id='333e52e9-e9ca-49f1-bce4-a03294dcf133', comment='agree')

        # use the created sub comment id to test
        r = fg.get_sub_comments(comment_id='ecc16bf1-7589-4ec9-b5c2-269c64697b90')
        print('Comment:', r)
    except Exception as e:
        tx.rollback()

def test7():
    # test get_player_comments
    tx = fg._graph.begin(autocommit=False)
    try:
        fg.create_comment(uni='ja1', comment='good', player_id='aardsda01')
        r1 = fg.get_player_comments(player_id='aardsda01')
        print('player comment:', json.dumps(r1, indent=2))

        r2 = fg.get_team_comments(team_id='BOS')
        print('team comment:', json.dumps(r2, indent=2))

    except Exception as e:
        tx.rollback()

def test8():
    # test get player by team
    tx = fg._graph.begin(autocommit=False)
    try:
        r = fg.get_players_by_team(team_id="BOS", yearid=2015)
        print('the player list:',json.dumps(r, indent=2))

    except Exception as e:
        tx.rollback()
# test1()
# test2()
# test3()
# test4()
# test5()
# test6()
#test7()
test8()