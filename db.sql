CREATE TABLE Location (
    GooglePlaceId INT PRIMARY KEY NOT NULL,
    Name          TEXT,
    Latitude      REAL            NOT NULL,
    Longitude     REAL            NOT NULL
);

CREATE TABLE University (
    UniversityID INT PRIMARY KEY NOT NULL,
    StudentCount INT             NOT NULL,
    Name         TEXT            NOT NULL,
    Description  TEXT,
    AvatarImage  LO,
    EmailDomain  TEXT            NOT NULL
);

CREATE TABLE UniversityLocation (
    GooglePlaceId INT NOT NULL,
    UniversityID  INT NOT NULL,
    FOREIGN KEY (GooglePlaceId) REFERENCES Location 
                          ON DELETE CASCADE
                          ON UPDATE CASCADE,
    FOREIGN KEY (UniversityID) REFERENCES University 
                          ON DELETE CASCADE
                          ON UPDATE CASCADE,
);

CREATE TABLE USER (
    UserID INT PRIMARY KEY NOT NULL,
    Email TEXT             NOT NULL,
    Password TEXT          NOT NULL,
);

CREATE TABLE SuperAdmin (
    UserID INT NOT NULL,
    FOREIGN KEY (UserID) REFERENCES User
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
);

CREATE TABLE StudiesAt (
    UserID       INT NOT NULL,
    UniversityID INT NOT NULL,
    FOREIGN KEY (UserID) REFERENCES User 
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
    FOREIGN KEY (UniversityID) REFERENCES University 
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
);

CREATE TABLE RSO (
    RSOID       INT PRIMARY KEY NOT NULL,
    Name        TEXT            NOT NULL,
    Description TEXT,
    AdminID     INT             NOT NULL,
    FOREIGN KEY (AdminID) REFERENCES User
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
);

CREATE TABLE RegisteredAt (
    RSOID           INT NOT NULL,
    UniversityID    INT NOT NULL,
    FOREIGN KEY (RSOID) REFERENCES RSO 
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
    FOREIGN KEY (UniversityID) REFERENCES University 
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
);

CREATE TABLE MemberOf (
    UserID          INT NOT NULL,
    RSOID           INT NOT NULL,
    FOREIGN KEY (UserID) REFERENCES User 
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
    FOREIGN KEY (RSOID) REFERENCES RSO 
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
);

CREATE TABLE Event (
   EventID        INT PRIMARY KEY NOT NULL,
   Summary        TEXT            NOT NULL,
   PrivacyLevel   INT             NOT NULL,
   Description    TEXT,
   Phone          TEXT,
   Email          TEXT,
   Dtstart        TIMESTAMP       NOT NULL,
   Dtend          TIMESTAMP       NOT NULL,
   Until          TIMESTAMP,
   Rrule          TEXT
);

CREATE TABLE EventLocation (
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
    Postdate  TIMESTAMP PRIMARY KEY NOT NULL,
    Text      TEXT                  NOT NULL,
    UserID    INT                   NOT NULL,
    EventID   INT                   NOT NULL,
    FOREIGN KEY (UserID) REFERENCES User 
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
    FOREIGN KEY (EventID) REFERENCES Event 
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
);

CREATE TABLE Organizes (
    RSOID           INT NOT NULL,
    EventID         INT NOT NULL,
    FOREIGN KEY (RSOID) REFERENCES RSO 
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
    FOREIGN KEY (EventID) REFERENCES Event 
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
);

CREATE EventTag (
    EventTagID   INT PRIMARY KEY NOT NULL,
    EventTagName TEXT            NOT NULL
);

CREATE TABLE EventCategory (
    EventID    INT NOT NULL,
    EventTagID INT NOT NULL,
    FOREIGN KEY (EventID) REFERENCES Event 
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
    FOREIGN KEY (EventTagID) REFERENCES EventTag
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
);