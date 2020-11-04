def expire_child_companies(mother, children_looked=0, children=None):
    """
    Expira empresas filhas quando a mãe é expirada 

    Args:
        mother (UserCompany): empresa mae.
        children_looked (int, optional): Contador que é usado como indice para andar nas empresas filhas. Defaults to 0.
    """

    if not children:
        children = mother.get_children()

    while children_looked < len(children):
        if children[children_looked].expires_at:
            children_looked += 1
            continue

        children[children_looked].expires_at = datetime.datetime.now()
        db.session.add(children[children_looked])

        UserCompanyResource.log_action_history_db_item(
            u'Data de expiração atualizada',
            u'A empresa teve a data de expiração atualizada via empresa mãe',
            children[children_looked].HISTORY_RESOURCE_ID,
            children[children_looked].id,
            commit=False
        )

        cur_uc_children = children[children_looked].get_children()

        if cur_uc_children:
            expire_child_companies(children[children_looked], children=cur_uc_children)

        children_looked += 1
