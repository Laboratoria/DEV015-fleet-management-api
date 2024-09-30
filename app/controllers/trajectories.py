from datetime import datetime
from flask import jsoniify
from sqlalchemy import func

from app.database.db import db
from app.models.taxis import taxis
from app.models.trajectories import trajectories