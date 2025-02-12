CREATE TABLE IF NOT EXISTS customers (
    customer_id INT NOT NULL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL, 
    money_spent DECIMAL NOT NULL,
    p_word TEXT NOT NULL,
    email TEXT NOT NULL,
    age INT NOT NULL
);

CREATE TABLE IF NOT EXISTS hotel_rooms (
    room_number INT NOT NULL PRIMARY KEY,
    no_beds INT NOT NULL,
    no_guests INT NOT NULL,
    price DECIMAL NOT NULL
);



CREATE TABLE IF NOT EXISTS animals (
    animal_id INT NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    class TEXT NOT NULL,
    latin_name TEXT NOT NULL,
    description TEXT NOT NULL,
    iucn_status TEXT NOT NULL,
    image_url TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bought_tickets (
    ticket_id INT NOT NULL PRIMARY KEY,
    ticket_type TEXT NOT NULL,
    ticket_date DATE NOT NULL,
    customer_id INT NOT NULL REFERENCES customers
);

CREATE TABLE IF NOT EXISTS reservations (
    reservation_id INT NOT NULL PRIMARY KEY,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    price DECIMAL NOT NULL,
    customer_id INT REFERENCES customers,
    room_number INT REFERENCES hotel_rooms
);

CREATE TABLE IF NOT EXISTS edu_reservation (
    edu_reservation_id INT NOT NULL PRIMARY KEY,
    visit_date DATE NOT NULL,
    visitors_amount INT NOT NULL
);

CREATE TABLE IF NOT EXISTS ticket_prices (
    child_price DECIMAL NOT NULL,
    adult_price DECIMAL NOT NULL,
    edu_price DECIMAL NOT NULL
);



INSERT INTO customers VALUES (0,'Mark', 'Gibson', 0.0, '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'markgibson@gmail.com', 18);
INSERT INTO customers VALUES (1,'Jim', 'Bob', 0.0, '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'jimbob@gmail.com', 18);
INSERT INTO customers VALUES (2,'Ross', 'Red', 0.0, '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'rossred@gmail.com', 18);
INSERT INTO customers VALUES (3,'Sophie', 'Potts', 0.0, '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'sophiepotts@gmail.com', 18);
INSERT INTO customers VALUES (4,'Kim', 'Kingley', 0.0, '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'kimkingley@gmail.com', 18);

INSERT INTO hotel_rooms VALUES (101, 1, 1, 50.0);
INSERT INTO hotel_rooms VALUES (102, 1, 2, 75.0);
INSERT INTO hotel_rooms VALUES (103, 2, 2, 85.0);
INSERT INTO hotel_rooms VALUES (104, 2, 3, 95.0);
INSERT INTO hotel_rooms VALUES (105, 3, 3, 105.0);
INSERT INTO hotel_rooms VALUES (106, 3, 4, 120.0);
INSERT INTO hotel_rooms VALUES (107, 4, 4, 130.0);
INSERT INTO hotel_rooms VALUES (108, 4, 5, 150.0);
INSERT INTO hotel_rooms VALUES (109, 1, 2, 75.0);
INSERT INTO hotel_rooms VALUES (110, 2, 2, 85.0);
INSERT INTO hotel_rooms VALUES (111, 2, 3, 95.0);
INSERT INTO hotel_rooms VALUES (112, 3, 3, 105.0);

INSERT INTO animals VALUES (0,'Red Panda','Mammal', 'Ailurus fulgens','The Red Panda is native to the eastern Himalayas and Southwest China. It weighs between 3.2 and 15kg and is well adapted to climbing due to its flexible joints and curved semi-retractile claws.','Endangered', 'red_panda');
INSERT INTO animals VALUES (1,'Amur Tiger','Mammal', 'Panthera tigris altaica', 'The Amur Tiger is a big cat primarily found in forests in Russia. They are known to use scent to mark their large territories.','Endangered', 'tiger');
INSERT INTO animals VALUES (2,'Siamese Crocodile','Reptile', 'Crocodylus siamensis','The Siamese Crocodile is native to Eastern Asia in areas such as Indonesia, Brunei, Vietnam and Thailand. It is a medium sized crocodile with a broad, smooth snoot. Overall it is olive green.','Critically Endangered', 'crocodile');
INSERT INTO animals VALUES (3,'Peregrine Falcon','Bird', 'Falco peregrinus','The Peregrine Falcon is the fastest animal on the planet, reaching over 200mph during dives after its prey. It is a bird of prey that is found nearly everywhere on earth excluding extreme polar regions, tropical rainforests and very high mountains.','Least Concern','falcon');
INSERT INTO animals VALUES (4,'Eagle','Bird', 'Haliaeetus albicilla','The White-Tailed Eagle, (or "Sea Eagle") is a large bird of prey found all across temperate areas in Europe and Asia. ','Least Concern','eagle');
INSERT INTO animals VALUES (5,'Komodo Dragon','Reptile', 'Varanus komodoensis','The Komodo Dragon is a large reptile that is found in the Indonesian islands of Komodo, Rinca, Flores, Gili Dasami and Gili Motang. They can grow up to 10 feet in length','Endangered', 'komodo_dragon');
INSERT INTO animals VALUES (6,'Barbary Ape','Mammal', 'Macaca sylvanus','The Barbary Ape is native to the Atlas Mountains of Algeria, Tunisia and Morocco. This species is interesting as males play an atypical role in rearing young, as they are integral to raising all infants.','Endangered', 'monkey');
INSERT INTO animals VALUES (7,'Giant Tortoise','Reptile', 'Aldabrachelys gigantea','The Aldabra Giant Tortoise is endemic to the Seychelles. They have an average weight of 250 kg in males and they generally eat grasses, leaves, woody plant stems and fruit.','Vulnerable','tortoise');
INSERT INTO animals VALUES (8,'Burmese Python','Reptile', 'Python bivittatus','The Burmese Python is one of the largest species of snakes that is native to Southeast Asia. It is a dark-soloured non-venomous snake with many brown blotches bordered by black down the back. They typically grow to 5m in the wild, however our specimens are over 7m in length!','Vulnerable','python');
INSERT INTO animals VALUES (9,'Penguin','Bird', 'Spheniscus magellanicus','The Magellanic Penguin is a South American penguin native to Argentina, Chile and the Falkland Isalnds. They grow to be 61-76cm tall and weigh between 2.7 and 6.5kg.','Least Concern', 'penguin');
INSERT INTO animals VALUES (10,'Frog','Amphibian', 'Agalychnis callidryas','The Red-Eyed Tree Frog is native to forests in Central America down to Northern South America. The species is known for its bright, vibrant green body with blue and yellow stripes on the side. They are nocturnal and do most of their hunting for insects at night.','Least Concern', 'frog');

