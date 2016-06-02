# coding: utf8
# try something like
def index():
    redirect(URL(c='admin', f='users'))

@auth.requires_membership('administrador')
def users():
    session.show_title = False
    db.auth_user.id.readable=False
    adminGroupID = db(db.auth_group.role == "administrador").select(db.auth_group.id).first()
    adminRow = db(db.auth_membership.group_id==adminGroupID).select().first()
    query = db.auth_user
    if adminRow != None:
        adminId = adminRow.user_id
        query=((db.auth_user.id != adminId))
    form = SQLFORM.grid(query=query, oncreate=addUserToGroup)
    title = T("Registered users")
    return dict(form=form, title=title)

def addUserToGroup(form):
    if form.vars.id:
        groupID = db(db.auth_group.role == "digitador").select(db.auth_group.id).first()
        db.auth_membership.insert(user_id=form.vars.id, group_id=groupID)
