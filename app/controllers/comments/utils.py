from typing import Dict, Any
from app.repositories.models import Comment
from typing import List, Dict, Any
from collections import OrderedDict, defaultdict

def _comment_to_dict(comment: Comment) -> Dict[str, Any]:
    """ Represent a Comment as a dictionary """
    return {
        "id": comment.id,
        "timestamp": comment.created_at,
        "content": comment.content,
        "author": {
            "id": comment.user.id,
            "name": comment.user.username
        },
        "post": {
            "id": comment.post.id,
            "title": comment.post.title
        },
        "parent": {
            "id": comment.parent_comment.id,
            "author": comment.parent_comment.user.username
        } if comment.parent_comment else None
    }

def users_return(comment, comments) -> Dict[str, Any]:
    for comments in comment:
        return {
            "post_id": comments["post"],
            "timestamp": comments["timestamp"],
            "author": {
                "id": comments["author"]["id"],
                "username": comments["author"]["name"]
            },
            "comments": build_comment_tree(comments)
        }

def _comment_return(comment: Comment) -> Dict[str, Any]:
    return {
        "id": comment.id,
        "content": comment.content,
        "parent": {
            "id": comment.parent_comment.id
        } if comment.parent_comment else ""
    }



# def build_comment_tree(comments):
#     """
#     Constrói uma estrutura de árvore para os comentários.
#     :param comments: Lista de comentários em formato plano.
#     :return: Lista de comentários raiz com as respostas aninhadas.
#     """
#     # Cria um mapa de ID -> comentário para acesso rápido
#     comment_list = [
#         _nem_comment_return(comment)
#         for comment in comments
#     ]

#     comment_map = {comment.id: _nem_comment_return(comment) for comment in comments}
#     roots = []

#     for comment in comment_list:

#         if comment["parent"] != "":  # Se o comentário possui um pai
#             id_pai = comment["parent"]["id"]
#             parent = comment_map[comment["parent"]["id"]]
#             if parent:
#                 try:
#                     comment_map[id_pai]["children"].append(comment)
#                 except Exception:
#                     comment_map[id_pai]["children"] = list()
#                     comment_map[id_pai]["children"].append(comment)

#     # # Reorganiza os dicionários para mover 'children' para o final
#     # for comment in comment_map.values():
#     #     if 'children' in comment:
#     #         # Remove e reanexa o 'children' para garantir que seja o último
#     #         children = comment.pop('children')
#     #         comment['children'] = children
    
#     for comment in comment_map.values():
#         comment.setdefault('children', [])

#     return comment_map

def build_comment_tree(comments) -> List[Dict]:
    """
    Constrói uma estrutura de árvore para os comentários.
    :param comments: Lista de comentários em formato plano.
    """
    # Cria um mapa de ID -> comentário para acesso rápido
    comment_map = {comment.id: _comment_return(comment) for comment in comments}

    roots = []  # Lista para armazenar os comentários raiz

    for comment in comments:
        parent_id = comment.parent_comment.id if comment.parent_comment else None

        if parent_id:
            # Adiciona o comentário como filho do pai
            parent = comment_map.get(parent_id)
            if parent:
                #Valida se existe a lista childre, se não existir, cria a lista
                try:
                    parent["children"].append(comment_map[comment.id])
                except Exception:
                    parent["children"] = list()
                    parent["children"].append(comment_map[comment.id])
        else:
            # Se não tiver pai, é um comentário raiz
            roots.append(comment_map[comment.id])

    #Garante que todos os comentários tenham a lista children
    for comment in comment_map.values():
        comment.setdefault('children', [])


    return roots

# if __name__ == "__main__":
#     comments = [
#   {
#     "id": 771,
#     "content": "Brother state blue computer say like. South wrong visit. Mission station weight.\nBuild work course campaign economic cut. Pressure computer cup respond black floor. Manager answer staff amount manage great.\nHeart arm another ok animal seek.",
#     "parent": {
#       "id": 312
#     }
#   },
#   {
#     "id": 550,
#     "content": "Different official protect. Commercial community according dream open decade light able.\nRecord well crime where skill almost whom approach. People mean put instead high have try.",
#     "parent": {
#       "id": 398
#     }
#   },
#   {
#     "id": 667,
#     "content": "Turn executive painting once little determine. Want floor poor third range but.\nFar magazine across draw.\nTree coach onto financial amount onto believe training. Worker attack others professor.",
#     "parent": {
#       "id": 490
#     }
#   },
#   {
#     "id": 625,
#     "content": "Human anyone occur real get rate stuff. Unit change specific. Address beat difficult water.\nBe stand course provide force mean contain. Keep court religious. Unit fight majority local develop.",
#     "parent": {
#       "id": 490
#     }
#   },
#   {
#     "id": 490,
#     "content": "Than technology writer whom. Some to evening speak near skill decade.\nQuite social mission view kid Congress hear focus. Former citizen join police hot decide north.",
#     "parent": {
#       "id": 227
#     }
#   },
#   {
#     "id": 564,
#     "content": "Model ball teach language always like. Film south management shoulder soldier. Information ten plan discuss serve child.\nExample film almost beat. Industry order outside because method number. May difference leader song rich imagine.",
#     "parent": {
#       "id": 329
#     }
#   },
#   {
#     "id": 398,
#     "content": "Treatment crime discussion inside writer. Support standard environment.\nArtist paper type anything note role theory. Will add up. Behind body image artist interesting continue direction someone.",
#     "parent": {
#       "id": 196
#     }
#   },
#   {
#     "id": 615,
#     "content": "Listen skin cell ask truth. Individual girl kind hot action space.\nTime land popular pass none consumer. Record worry west music finish cut. Front seven structure though somebody major. Trial town call risk.",
#     "parent": {
#       "id": 312
#     }
#   },
#   {
#     "id": 573,
#     "content": "Goal tend develop involve. Report late only democratic require add court. Authority and many heart source.\nFree attention also. Thought community arrive direction position authority eat. Purpose economic parent upon list.",
#     "parent": {
#       "id": 339
#     }
#   },
#   {
#     "id": 312,
#     "content": "Position either name drug feeling director science must. Adult amount perform buy edge surface.\nPlant shoulder scene sing know. Night likely thought focus responsibility who.\nExpert organization century speech.",
#     "parent": {
#       "id": 135
#     }
#   },
#   {
#     "id": 329,
#     "content": "Herself say really between write success. Somebody white look serve. Reach quite training break difficult yes.\nNothing church movie everything seem while. First option need contain fire. Even significant player blue federal.",
#     "parent": {
#       "id": 196
#     }
#   },
#   {
#     "id": 348,
#     "content": "Threat law speech final possible fund should individual. Report guess difference skill enough believe.\nOrganization both fund ball. Sea person pattern front structure stop.",
#     "parent": {
#       "id": 227
#     }
#   },
#   {
#     "id": 196,
#     "content": "Eight home to story tree.\nWould sure candidate professor author management expect. Way social statement exist across beyond than. Son less condition day room decide later debate.\nHim edge listen cup they. Fact range bed idea know risk.",
#     "parent": {
#       "id": 103
#     }
#   },
#   {
#     "id": 509,
#     "content": "On although southern force share. Defense although no base imagine court.\nOften those your suddenly forward than. Establish value either very later difference scientist.\nUp himself bed executive various.",
#     "parent": {
#       "id": 202
#     }
#   },
#   {
#     "id": 227,
#     "content": "Beat him week specific form force exactly. Top candidate education total. Right memory within allow everything.\nIndeed personal past yourself. Well region rise dog second.",
#     "parent": {
#       "id": 16
#     }
#   },
#   {
#     "id": 677,
#     "content": "To worker business region step. Shoulder expert per hit mother film start help. Analysis general contain market rich.\nMillion call coach teach watch about break. Prepare go deal.",
#     "parent": {
#       "id": 327
#     }
#   },
#   {
#     "id": 339,
#     "content": "Source prepare once. Low of police manager everything democratic take writer. Gun skill voice poor.\nTrouble capital report consumer show. Party million hour likely who whom.",
#     "parent": {
#       "id": 239
#     }
#   },
#   {
#     "id": 711,
#     "content": "Local personal guy just lead and. Receive future station run. Local with affect pretty although natural explain.\nShort surface consider sing nothing about reach interest. Which down though management material.",
#     "parent": {
#       "id": 487
#     }
#   },
#  { 
#     "id": 400,
#     "content": "Page ago head. Sound first model. Space after research leader image us relate.\nThreat view memory away partner movie everybody. Wonder mean probably look article race. Avoid officer door wife though these institution.",
#     "parent": {
#       "id": 229
#     }
#   },
#   {
#     "id": 671,
#     "content": "Fly owner ok eye city. What nice although throughout resource close decide mother. What probably church story president inside media design.\nSerious kid according spring.",
#     "parent": {
#       "id": 337
#     }
#   },
#   {
#     "id": 337,
#     "content": "Baby morning central. Admit effort gun total. His although lawyer arm out.\nUnderstand think various although natural onto. Everyone account authority recognize. Science east bed culture example under whom.",
#     "parent": {
#       "id": 187
#     }
#   },
#   {
#     "id": 561,
#     "content": "Accept control Mr trip response. Long strategy degree also happen opportunity need. Process small very happy dinner.\nKey next whose attention station. All scientist law new water operation. Detail put spend other consider subject financial.",
#     "parent": {
#       "id": 327
#     }
#   },
#   {
#     "id": 562,
#     "content": "Yes likely listen read certainly eye. Late activity affect read including.\nTrouble plant college face center class. Old may wrong might recognize.\nAvailable law PM quickly six. Kid into size record.",
#     "parent": {
#       "id": 328
#     }
#   },
#   {
#     "id": 327,
#     "content": "By Mr decision go service tree nation. World quite until young player but wind.\nTime later once lead majority both. Dog film I send.",
#     "parent": {
#       "id": 202
#     }
#   },
#   {
#     "id": 328,
#     "content": "Authority feeling its food protect none. Recent parent collection without try mind green.\nOwner almost walk significant health special. Pull personal point old less. Able my avoid.\nBill box serve. Store resource even various the.",
#     "parent": {
#       "id": 229
#     }
#   },
#   {
#     "id": 229,
#     "content": "Free play present popular man maintain know base. Suddenly Republican machine across. Fall try send Congress involve top cover.\nSend bed child.\nNewspaper away measure force able court southern. Right carry old five senior story.",
#     "parent": {
#       "id": 72
#     }
#   },
#   {
#     "id": 583,
#     "content": "Compare board sometimes over. Require example score region major green will west.\nOrganization price director land market. Claim reflect perform drive attorney section store. Itself wonder significant show.",
#     "parent": {
#       "id": 498
#     }
#   },
#   {
#     "id": 847,
#     "content": "Necessary bring much return. Theory similar itself beat build open.\nRecent dog source. Activity social may really stock simply next.\nIndicate major test nor process. Stop stop type high father perhaps before.",
#     "parent": {
#       "id": 487
#     }
#   },
#   {
#     "id": 744,
#     "content": "Make paper behavior unit lose. Campaign popular since anyone. Pick write feeling language they per.\nAct forward good best road.\nStudy must adult blood anyone national magazine impact.",
#     "parent": {
#       "id": 467
#     }
#   },
#   {
#     "id": 750,
#     "content": "Company wind write question. Move everybody along hard daughter so. Sell hold reach.\nThus send enough pass right hard next. Rise call administration surface plant.\nThem beat paper natural style eight often. Pay return fact factor detail evening.",
#     "parent": {
#       "id": 467
#     }
#   },
#   {
#     "id": 591,
#     "content": "Begin often gas race start western win. Guy something act ago hope.\nHerself its much a all. Morning image cover clear collection edge.\nStaff plant but new goal ask skill.",
#     "parent": {
#       "id": 487
#     }
#   },
#   {
#     "id": 487,
#     "content": "Factor ok claim of no music month. Through choose sing but.\nCrime religious unit rock watch especially stock. Personal commercial boy individual. Investment sign herself watch.",
#     "parent": {
#       "id": 135
#     }
#   },
#   {
#     "id": 496,
#     "content": "Herself talk it meet popular. Bring result use others. Cup window individual which effort there behind level.\nRecord election country six next down could. Important economic today offer. Police agent woman possible statement wind film.",
#     "parent": {
#       "id": 135
#     }
#   },
#   {
#     "id": 202,
#     "content": "Thus course answer black defense. Way green discuss director catch involve argue.\nShare toward standard same. White side close together the resource ability. You catch wall friend factor policy. Tell girl too what kind too.",
#     "parent": {
#       "id": 32
#     }
#   },
#   {
#     "id": 221,
#     "content": "Matter particularly return state agreement. News old everyone themselves make.\nAlone want cost hour. Five place camera old thought sport outside. You along report hundred force accept.",
#     "parent": {
#       "id": 103
#     }
#   },
#   {
#     "id": 159,
#     "content": "Teacher including operation experience thought perform government. Usually son measure.\nRecord anything local clearly. Serve understand who provide speak.",
#     "parent": {
#       "id": 32
#     }
#   },
#   {
#     "id": 241,
#     "content": "Here ready truth reality Democrat. Significant candidate fill early behind popular. Rate glass director company nation.\nWhatever game picture. Machine pretty hand sister many form.",
#     "parent": {
#       "id": 100
#     }
#   },
#   {
#     "id": 67,
#     "content": "Protect tonight today on tend lot lose.\nProve doctor world may from memory look. Sport structure action bed within room position.\nBoth quality two paper. Star check allow mother network pattern. Management use end point war which ready.",
#     "parent": ""
#   },
#   {
#     "id": 144,
#     "content": "Because score true source. Son bad alone expect spend energy sell.\nMember experience no various heavy significant them. Civil thus explain. Success performance doctor two foot.",
#     "parent": {
#       "id": 58
#     }
#   },
#   {
#     "id": 135,
#     "content": "Serious hair doctor eat. Me statement million eight seven.\nExecutive nature training source surface.\nSeem amount section large maintain candidate large.",
#     "parent": {
#       "id": 16
#     }
#   },
#   {
#     "id": 498,
#     "content": "Responsibility help one accept. Language rather food store term. Study relationship structure deal.\nCollege vote change available name either. Test hot authority purpose. Avoid radio suffer kind.",
#     "parent": {
#       "id": 187
#     }
#   },
#   {
#     "id": 467,
#     "content": "Sell camera simply at feel our news. Commercial bank beautiful news.\nLawyer camera government boy appear. Talk nor whether gun. Toward only discuss especially natural.\nPut probably significant for student true. Sense clear number.",
#     "parent": {
#       "id": 239
#     }
#   },
#   {
#     "id": 239,
#     "content": "Throw southern important green across. Most drop become. Design up site indicate adult get design.\nLeg two teacher try serve few building worry. Including century near act loss building wear.",
#     "parent": {
#       "id": 103
#     }
#   },
#   {
#     "id": 248,
#     "content": "Thank especially majority doctor scene international. Many leave difference.\nMusic effect raise.\nRecent staff choose hit either friend dream.\nSea trial challenge continue. Eat have hundred produce above car.",
#     "parent": {
#       "id": 72
#     }
#   },
#   {
#     "id": 187,
#     "content": "Economy community market. Factor wonder member training establish. Moment money ahead say voice.\nDevelopment government authority open itself defense impact factor.\nReally film her expect individual quickly stand. Time against training more risk.",
#     "parent": {
#       "id": 16
#     }
#   },
#   {
#     "id": 58,
#     "content": "Rise fast official west still personal. Throughout new ready listen western enjoy old.\nMouth general public second. Sea teacher rate floor employee five key. Father of investment understand run idea doctor another.",
#     "parent": ""
#   },
#   {
#     "id": 32,
#     "content": "Money memory house in. Industry bring million new something conference. Power note red describe.\nAlong to member season seven. Quickly organization throughout continue without.",
#     "parent": ""
#   },
#   {
#     "id": 103,
#     "content": "End share foot community majority. Their purpose then whether section role. Old without behind beat world.\nLearn individual front understand. Serve nor last blue well affect project.",
#     "parent": ""
#   },
#   {
#     "id": 23,
#     "content": "Crime appear last cell evening mother wall.\nEverybody guess little relationship cultural citizen natural. Plan control exist audience might as. Never it southern.",
#     "parent": ""
#   },
#   {
#     "id": 100,
#     "content": "Run defense ahead. Clear cover hot if cold consider teach. Throughout area wife science of environment option offer. Police energy according check become.\nMoney two myself TV. The young everyone standard simply. Answer five state.",
#     "parent": ""
#   },
#   {
#     "id": 16,
#     "content": "Practice realize low same put similar experience. Realize relationship consider trial major.\nHold democratic practice interesting local. Brother top poor why scene dream real. Benefit score account speech show.",
#     "parent": ""
#   },
#   {
#     "id": 72,
#     "content": "Letter fear not hit paper little. Two I front professional certain eat standard.\nForm cause party American. Item certain tell again heart get.\nSing professor concern word act. Forget child control college green candidate purpose growth.",
#     "parent": ""
#   },
#   {
#     "id": 31,
#     "content": "Rise free same security government true seem. On suffer learn process usually in recognize find. Require size democratic loss growth remember draw include.",
#     "parent": ""
#   }
# ]


#     build_comment_tree(comments)