from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    genres = db.Column(db.PickleType, nullable=False)
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(500))
    looking_for_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(), nullable=True)
    upcoming_shows = db.Column(db.PickleType, nullable=True)
    past_shows = db.Column(db.PickleType, nullable=True)
    past_shows_count = db.Column(db.Integer, default=0, nullable=True)
    upcoming_shows_count = db.Column(db.Integer, default=0, nullable=True)

    def __repr__(self) -> str:
        return f'id:{self.id} name:{self.name} genres: {self.genres} city: {self.city} state: {self.state}'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(500))
    looking_for_venues = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(), nullable=True)
    upcoming_shows = db.Column(db.PickleType, nullable=True, default=[])
    past_shows = db.Column(db.PickleType, nullable=True, default=[])
    past_shows_count = db.Column(db.Integer, default=0, nullable=True)
    upcoming_shows_count = db.Column(db.Integer, default=0, nullable=True)

    def __repr__(self) -> str:
        return f'id:{self.id} name:{self.name} genres: {self.genres} city: {self.city} state: {self.state}'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.String())

    def updateRecords(self, Artist, Venue):

        artist = Artist.query.get(self.artist_id)
        venue = Venue.query.get(self.venue_id)
        if artist != null and venue != null:
            venueRecordArtist = {
                "artist_id": self.artist_id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": self.start_time
            }

            artistRecordVenue = {
                "venue_id": self.venue_id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": self.start_time
            }

            date = format_datetime(self.start_time)
            dateArray = date.split(',')
            year = dateArray[-1][:5]

            if int(year) < int(datetime.today().year):
                try:
                    artistData = list(artist.past_shows)
                    venueData = list(venue.past_shows)
                    artistData.append(artistRecordVenue)
                    venueData.append(venueRecordArtist)
                    currentCount = int(artist.past_shows_count) + 1
                    venueCurrentCount = int(venue.past_shows_count) + 1
                    artist.past_shows = artistData
                    artist.past_shows_count = currentCount
                    venue.past_shows = venueData
                    venue.past_shows_count = venueCurrentCount
                    db.session.commit()
                except:
                    print(sys.exc_info)
                finally:
                    db.session.close()

            elif int(year) > int(datetime.today().year):
                try:
                    artistData = list(artist.upcoming_shows)
                    artistData.append(artistRecordVenue)
                    currentCount = int(artist.upcoming_shows_count) + 1
                    artist.upcoming_shows = artistData
                    artist.upcoming_shows_count = currentCount
                    venueData = list(venue.upcoming_shows)
                    venueData.append(venueRecordArtist)
                    venueCurrentCount = int(venue.upcoming_shows_count) + 1
                    venue.upcoming_shows = venueData
                    venue.upcoming_shows_count = venueCurrentCount
                    db.session.commit()
                except:
                    pass
                finally:
                    db.session.close()
            else:
                try:
                    artistData = list(artist.upcoming_shows)
                    artistData.append(artistRecordVenue)
                    currentCount = int(artist.upcoming_shows_count) + 1
                    artist.upcoming_shows = artistData
                    artist.upcoming_shows_count = currentCount
                    venueData = list(venue.upcoming_shows)
                    venueData.append(venueRecordArtist)
                    venueCurrentCount = int(venue.upcoming_shows_count) + 1
                    venue.upcoming_shows = venueData
                    venue.upcoming_shows_count = venueCurrentCount
                    db.session.commit()
                except:
                  pass
                finally:
                    db.session.close()

        else:
            return 'invalid ids'
