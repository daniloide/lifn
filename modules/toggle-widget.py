# -*- coding: utf-8 -*-
from gluon import html
def widget(field, value):
    """
    """
    wrapper = html.DIV(
        _class="btn-group",
        _id="toggle-button-div-%s-%s" % (field._tablename,field.name),
        **{'_data-toggle':'buttons-radio'}
        )
    inp = html.INPUT(
        _id=field.name,
        _name=field._tablename,
        #_style="display:none;",
        _value=field.name,
        _type="radio"
    )
    btnYes = html.BUTTON(
        T("Yes"),
        _class="toggle-btn %s btn" % ("noactive"),
        _id="%s_Yes" % (field.name),
        _onclick="document.getElementById('%s').checked = true;" % (field.name),
        _type="button"
    )
    btnNo = html.BUTTON(
        T("No"),
        _class="toggle-btn %s btn" % ("noactive"),
        _id="%s_No" % (field.name),
        _onclick="document.getElementById('%s').checked = false;" % (field.name),
        _type="button"
    )

    wrapper.components.extend([inp,btnYes, btnNo])
    print wrapper
    return wrapper
