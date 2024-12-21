from pixegami_hellos import create_app
from pixegami_hellos.organizations import Organizations
from pixegami_hellos.cam_db_config import db


app = create_app()


with app.app_context():
    
    new_org = Organizations(org_name="d8ew", csp_id=1) 
    db.session.add(new_org)
    db.session.commit()

    
    organizations = Organizations.query.all()
    for org in organizations:
        print(org.org_name)
