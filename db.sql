CREATE TABLE Event (
   EventID  INT PRIMARY KEY NOT NULL,
   Summary        TEXT      NOT NULL,
   Description    TEXT,
   Phone          TEXT,
   Email          TEXT,
   Dtstart        TIMESTAMP NOT NULL,
   Dtend          TIMESTAMP NOT NULL,
   Dtstart        TIMESTAMP NOT NULL,
   Until          TIMESTAMP NOT NULL,
   Rrule          TEXT,
);

CREATE TABLE Location (
    GooglePlaceId   INT PRIMARY KEY NOT NULL,
    Name            TEXT,
    Latitude        REAL            NOT NULL,
    Longitude       REAL            NOT NULL
);

CREATE TABLE LocatedAt (
    GooglePlaceId   INT NOT NULL,
    EventID         INT NOT NULL,
    FOREIGN KEY (GooglePlaceId) REFERENCES Location 
                          ON DELETE CASCADE
                          ON UPDATE CASCADE,
    FOREIGN KEY (EventID) REFERENCES Event 
                          ON DELETE CASCADE
                          ON UPDATE CASCADE,
);

CREATE TABLE Comment (
    EventID       INT       NOT NULL,
    UserID        INT       NOT NULL,
    PostTimestamp TIMESTAMP NOT NULL,
    Text          TEXT      NOT NULL,
    Rating        INT      NOT NULL,
    PRIMARY KEY (PostTimestamp),
    FOREIGN KEY (EventID) REFERENCES Event 
                          ON DELETE CASCADE
                          ON UPDATE CASCADE,
    FOREIGN KEY (UserID) REFERENCES User 
                          ON DELETE CASCADE
                          ON UPDATE CASCADE,
);