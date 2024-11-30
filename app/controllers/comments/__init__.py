from collections import defaultdict
import json
from typing import List
from werkzeug.exceptions import NotFound
from flask import Blueprint, Response, jsonify


from app.repositories import comments
from app.repositories.models import Comment
from app.repositories.users import get_user_comments

from .utils import _comment_to_dict, build_comment_tree, users_return
from app.repositories.comments import get_all_comments, get_post_comments


BLUEPRINT = Blueprint('comments', __name__)


@BLUEPRINT.route('/comments')
def get_all_posts():
    return jsonify([
        _comment_to_dict(comment)
        for comment in get_all_comments()
    ])


@BLUEPRINT.route('/comments/<comment_id>')
def get_comment_by_id(comment_id):
    comment = comments.get_comment_by_id(comment_id)

    if comment is None:
        raise NotFound

    return jsonify(_comment_to_dict(comment))


@BLUEPRINT.route('/posts_anterior/<post_id>/comments')
def get_comments_from_post_before(post_id):
    return jsonify([
        _comment_to_dict(comment)
        for comment in comments.get_post_comments(post_id)
    ])


@BLUEPRINT.route('/posts/<post_id>/comments')
def get_comments_from_post(post_id):
    comments = get_post_comments(post_id)
    tree = build_comment_tree(comments)
    response_data = json.dumps(tree, ensure_ascii=False)  
    return Response(response_data, mimetype='application/json')


# @BLUEPRINT.route('/users/<user_id>/comments')
# def get_comments_by_user(user_id):
#     comments = get_user_comments(user_id)
#     # grouped_comments_dict = dict(comments)
    
#     # return grouped_comments_dict




#     # Agrupa os comentários pelo post_id 
#     grouped_comments = defaultdict(list)

#     for comment in comments:
#         post_id = comment.post_id
#         grouped_comments[post_id].append(_comment_to_dict(comment))

#     response = []


#     for post_id, post_comments in grouped_comments.items():
#         # Pega o primeiro comentário para recuperar dados do post
#         post_comment_dict = {post_id: post_comments}
#         # Ajusta a chamada à função users_return

        

#         response_dict = users_return(post_comments, comments)  

#         response.append(response_dict)
#         return dict(response)

#     # Converte para JSON e retorna a resposta
#     response_data = json.dumps(response, ensure_ascii=False)  
#     return Response(response_data, mimetype='application/json')

BLUEPRINT = Blueprint('users', __name__)

@BLUEPRINT.route('/users/<user_id>/comments')
def get_user_comments_route(user_id):
    """
    Retorna as árvores de comentários relacionadas ao usuário.
    """
    user_comments = get_user_comments_with_relationships(user_id)
    comment_trees = build_user_comment_trees(user_comments)
    return jsonify(comment_trees)

def get_user_comments_with_relationships(user_id: int) -> List[Comment]:
    """
    Retorna todos os comentários de um usuário com informações relacionadas.
    Inclui os comentários pais e filhos.
    """
    # Busca os comentários do usuário
    comments = (
        Comment.query
        .filter(Comment.user_id == user_id)
        .all()
    )

    return comments


def build_user_comment_trees(user_comments: List[Comment]) -> List[Dict]:
    """
    Constrói as árvores de comentários relacionadas a um usuário.
    """
    def add_parents(comment, comments_map):
        """
        Adiciona todos os pais do comentário.
        """
        current = comment.parent_comment
        tree = comments_map[comment.id]
        while current:
            parent_tree = _comment_to_dict(current)
            parent_tree.setdefault("children", []).append(tree)
            tree = parent_tree
            current = current.parent_comment
        return tree

    def add_children(comment, comments_map):
        """
        Adiciona todos os filhos do comentário.
        """
        tree = comments_map[comment.id]
        for child in comment.children:
            child_tree = add_children(child, comments_map)
            tree.setdefault("children", []).append(child_tree)
        return tree

    comments_map = {comment.id: _comment_to_dict(comment) for comment in user_comments}
    trees = []

    for comment in user_comments:
        # Adiciona pais e filhos
        root = add_parents(comment, comments_map)
        root = add_children(comment, comments_map)

        # Garante que seja um nó raiz
        if not root.get("parent"):
            trees.append(root)

    return trees

# if __name__ == "__main__":
#     comments = [{
#   "comments": [
#     {
#       "author": {
#         "id": 59, 
#         "name": "Laura Clark"
#       }, 
#       "content": "Sing movement establish world letter. Understand professor son around save.\nCoach strategy article control serve attack. Old reflect rate sister prove street. Difference over senior social long drive.\nWorld themselves since very about before.", 
#       "id": 665, 
#       "parent": {
#         "author": "Nicole Hartman", 
#         "id": 441
#       }, 
#       "post": {
#         "id": 12, 
#         "title": "Table owner already memory."
#       }, 
#       "timestamp": "Fri, 29 Nov 2024 17:58:36 GMT"
#     }, 
#     {
#       "author": {
#         "id": 59, 
#         "name": "Laura Clark"
#       }, 
#       "content": "Mission onto light tell almost after. This project lawyer gun.\nSure term against something thing. Spring camera debate well particular purpose fall. Thank these your deal exactly middle tell Congress. Better back low themselves themselves.", 
#       "id": 725, 
#       "parent": {
#         "author": "Jennifer Ford", 
#         "id": 448
#       }, 
#       "post": {
#         "id": 4, 
#         "title": "Watch someone watch fund concern worry value."
#       }, 
#       "timestamp": "Fri, 29 Nov 2024 16:54:37 GMT"
#     }, 
#     {
#       "author": {
#         "id": 59, 
#         "name": "Laura Clark"
#       }, 
#       "content": "Decide surface right early visit. Seat pretty color security mind TV center. Become bank anything beyond contain station. Often free story.\nProject cup medical late. Teacher interesting magazine make compare ask.", 
#       "id": 664, 
#       "parent": {
#         "author": "Karl Soto", 
#         "id": 494
#       }, 
#       "post": {
#         "id": 13, 
#         "title": "Safe clearly artist top myself."
#       }, 
#       "timestamp": "Fri, 29 Nov 2024 16:04:00 GMT"
#     }, 
#     {
#       "author": {
#         "id": 59, 
#         "name": "Laura Clark"
#       }, 
#       "content": "Treatment together west value large foreign during.\nProfessor present speech almost. Sing none interview maybe low deep task.", 
#       "id": 545, 
#       "parent": {
#         "author": "Laura Clark", 
#         "id": 306
#       }, 
#       "post": {
#         "id": 9, 
#         "title": "A pattern cost."
#       }, 
#       "timestamp": "Wed, 27 Nov 2024 07:33:15 GMT"
#     }, 
#     {
#       "author": {
#         "id": 59, 
#         "name": "Laura Clark"
#       }, 
#       "content": "Threat bad dinner present. Fight have report body. Any especially today notice month environmental.\nCareer radio she himself any write. Expect threat together old magazine appear.", 
#       "id": 666, 
#       "parent": {
#         "author": "James Hunt", 
#         "id": 353
#       }, 
#       "post": {
#         "id": 15, 
#         "title": "Expect turn share imagine night foreign stage."
#       }, 
#       "timestamp": "Tue, 26 Nov 2024 23:16:58 GMT"
#     }, 
#     {
#       "author": {
#         "id": 59, 
#         "name": "Laura Clark"
#       }, 
#       "content": "After person give project. Situation easy over maintain campaign common. Cause scientist good simply training medical part.\nIn force me whatever sing sport. Sing all subject begin such morning.\nIndeed story Mr control.", 
#       "id": 663, 
#       "parent": {
#         "author": "Juan Lopez", 
#         "id": 358
#       }, 
#       "post": {
#         "id": 10, 
#         "title": "Structure list something want hard catch partner phone."
#       }, 
#       "timestamp": "Tue, 26 Nov 2024 19:55:11 GMT"
#     }, 
#     {
#       "author": {
#         "id": 59, 
#         "name": "Laura Clark"
#       }, 
#       "content": "Nice give talk page career stand. Magazine agree usually.\nBoy actually institution challenge instead family maybe. Rock environmental board explain. Economic accept everyone action receive.", 
#       "id": 662, 
#       "parent": {
#         "author": "Robert Shaw", 
#         "id": 482
#       }, 
#       "post": {
#         "id": 11, 
#         "title": "Station because end me stop growth."
#       }, 
#       "timestamp": "Thu, 21 Nov 2024 18:09:50 GMT"
#     }, 
#     {
#       "author": {
#         "id": 59, 
#         "name": "Laura Clark"
#       }, 
#       "content": "Small nearly current PM care service big star.\nEasy brother physical maintain. Affect into argue into seven.\nQuestion sense meeting when receive goal. Those anything take bit blue miss. Maybe officer wife claim compare fall price.", 
#       "id": 165, 
#       "parent": {
#         "author": "Emily Kline", 
#         "id": 49
#       }, 
#       "post": {
#         "id": 13, 
#         "title": "Safe clearly artist top myself."
#       }, 
#       "timestamp": "Mon, 18 Nov 2024 19:12:14 GMT"
#     }, 
#     {
#       "author": {
#         "id": 59, 
#         "name": "Laura Clark"
#       }, 
#       "content": "Local pass development real keep central often. See write performance fire event edge relationship.\nName successful general enough popular. Represent majority person leader article yes. South ask generation doctor song machine off.", 
#       "id": 306, 
#       "parent": {
#         "author": "Joshua Johnson", 
#         "id": 118
#       }, 
#       "post": {
#         "id": 9, 
#         "title": "A pattern cost."
#       }, 
#       "timestamp": "Sun, 17 Nov 2024 19:11:53 GMT"
#     }, 
#     {
#       "author": {
#         "id": 59, 
#         "name": "Laura Clark"
#       }, 
#       "content": "Suddenly PM have offer edge rule country. Blood simple sound east. Military skill season describe success fish. List role cut office find point four.", 
#       "id": 364, 
#       "parent": {
#         "author": "Megan Sanchez", 
#         "id": 250
#       }, 
#       "post": {
#         "id": 11, 
#         "title": "Station because end me stop growth."
#       }, 
#       "timestamp": "Sat, 16 Nov 2024 03:40:09 GMT"
#     }, 
#     {
#       "author": {
#         "id": 59, 
#         "name": "Laura Clark"
#       }, 
#       "content": "Left enter bar style. Arm leader final one entire as.\nCenter well list energy mission animal. Me yes choice road operation stand something.\nTest structure suddenly rate your at forward. Huge miss phone they. Step policy argue surface with born.", 
#       "id": 661, 
#       "parent": {
#         "author": "Laura Butler", 
#         "id": 266
#       }, 
#       "post": {
#         "id": 9, 
#         "title": "A pattern cost."
#       }, 
#       "timestamp": "Sun, 27 Oct 2024 09:13:57 GMT"
#     }
#   ]
# }]
    
# get_comments_by_user(comments)