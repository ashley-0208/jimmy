CREATE DATABASE StudentDB;
GO

USE StudentDB;
GO

CREATE TABLE StudentInfo (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    FullName NVARCHAR(100) NOT NULL,
    Major NVARCHAR(100) NOT NULL,
    Semester INT NOT NULL
);
GO

-- (Optional) Sample data for testing
INSERT INTO StudentInfo (FullName, Major, Semester) VALUES
(N'John Doe', N'Computer Science', 5),
(N'Jane Smith', N'Electrical Engineering', 3),
(N'Ali Rezaei', N'Software Engineering', 7);
GO
