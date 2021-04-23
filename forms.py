from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired

language_choices = [('al', 'Albanian'),
                    ('sq', 'Albanian'),
                    ('ar', 'Arabic'),
                    ('hy', 'Armenian'),
                    ('bp', 'Brazilian Portuguese'),
                    ('bg', 'Bulgarian'),
                    ('cf', 'Canadian French'),
                    ('ca', 'Catalan, Valencian'),
                    ('cn', 'Chinese (Simplified)'),
                    ('zh', 'Chinese (Simplified)'),
                    ('b5', 'Chinese (Traditional)'),
                    ('hr', 'Croatian'),
                    ('cs', 'Czech'),
                    ('dk', 'Danish'),
                    ('da', 'Danish'),
                    ('nl', 'Dutch'),
                    ('en', 'English'),
                    ('et', 'Estonian'),
                    ('fi', 'Finnish'),
                    ('fl', 'Flemish'),
                    ('fr', 'French'),
                    ('ka', 'Georgian'),
                    ('de', 'German'),
                    ('el', 'Greek (modern)'),
                    ('he', 'Hebrew'),
                    ('hi', 'Hindi'),
                    ('hu', 'Hungarian'),
                    ('id', 'Indonesian'),
                    ('it', 'Italian'),
                    ('ja', 'Japanese'),
                    ('ko', 'Korean'),
                    ('lv', 'Latvian'),
                    ('lt', 'Lithuanian'),
                    ('ms', 'Malay'),
                    ('mn', 'Mongolian'),
                    ('no', 'Norwegian'),
                    ('pl', 'Polish'),
                    ('pt', 'Portuguese'),
                    ('ro', 'Romanian, Moldavian, Moldovan'),
                    ('ru', 'Russian'),
                    ('sr', 'Serbian'),
                    ('sk', 'Slovak'),
                    ('sl', 'Slovenian'),
                    ('es', 'Spanish, Castilian'),
                    ('sv', 'Swedish'),
                    ('th', 'Thai'),
                    ('tr', 'Turkish'),
                    ('ua', 'Ukrainian'),
                    ('uk', 'Ukrainian'),
                    ('vi', 'Vietnamese')]

country_choices = [('AD', 'Andorra'),
                   ('AE', 'United Arab Emirates'),
                   ('AF', 'Afghanistan'),
                   ('AG', 'Antigua And Barbuda'),
                   ('AI', 'Anguilla'),
                   ('AL', 'Albania'),
                   ('AM', 'Armenia'),
                   ('AN', 'Netherlands Antilles'),
                   ('AO', 'Angola'),
                   ('AQ', 'Antarctica'),
                   ('AR', 'Argentina'),
                   ('AS', 'American Samoa'),
                   ('AT', 'Austria'),
                   ('AU', 'Australia'),
                   ('AW', 'Aruba'),
                   ('AZ', 'Azerbaijan'),
                   ('BA', 'Bosnia And Herzegowina'),
                   ('BB', 'Barbados'),
                   ('BD', 'Bangladesh'),
                   ('BE', 'Belgium'),
                   ('BF', 'Burkina Faso'),
                   ('BG', 'Bulgaria'),
                   ('BH', 'Bahrain'),
                   ('BI', 'Burundi'),
                   ('BJ', 'Benin'),
                   ('BM', 'Bermuda'),
                   ('BN', 'Brunei Darussalam'),
                   ('BO', 'Bolivia'),
                   ('BR', 'Brazil'),
                   ('BS', 'Bahamas'),
                   ('BT', 'Bhutan'),
                   ('BV', 'Bouvet Island'),
                   ('BW', 'Botswana'),
                   ('BY', 'Belarus'),
                   ('BZ', 'Belize'),
                   ('CA', 'Canada'),
                   ('CC', 'Cocos (Keeling) Islands'),
                   ('CD', 'Congo, The Democratic Republic Of The'),
                   ('CF', 'Central African Republic'),
                   ('CG', 'Congo'),
                   ('CH', 'Switzerland'),
                   ('CI', 'Cote D’ivoire'),
                   ('CK', 'Cook Islands'),
                   ('CL', 'Chile'),
                   ('CM', 'Cameroon'),
                   ('CN', 'China'),
                   ('CO', 'Colombia'),
                   ('CR', 'Costa Rica'),
                   ('CV', 'Cape Verde'),
                   ('CW', 'Curaçao'),
                   ('CX', 'Christmas Island'),
                   ('CY', 'Cyprus'),
                   ('CZ', 'Czech Republic'),
                   ('DE', 'Germany'),
                   ('DJ', 'Djibouti'),
                   ('DK', 'Denmark'),
                   ('DM', 'Dominica'),
                   ('DO', 'Dominican Republic'),
                   ('DZ', 'Algeria'),
                   ('EC', 'Ecuador'),
                   ('EE', 'Estonia'),
                   ('EG', 'Egypt'),
                   ('EH', 'Western Sahara'),
                   ('ER', 'Eritrea'),
                   ('ES', 'Spain'),
                   ('ET', 'Estonia'),
                   ('FI', 'Finland'),
                   ('FJ', 'Fiji'),
                   ('FK', 'Falkland Islands (Malvinas)'),
                   ('FM', 'Micronesia, Federated States Of'),
                   ('FO', 'Faroe Islands'),
                   ('FR', 'France'),
                   ('FX', 'France, Metropolitan'),
                   ('GA', 'Gabon'),
                   ('GB', 'Great Britain'),
                   ('GD', 'Grenada'),
                   ('GE', 'Georgia'),
                   ('GF', 'French Guiana'),
                   ('GH', 'Ghana'),
                   ('GI', 'Gibraltar'),
                   ('GL', 'Greenland'),
                   ('GM', 'Gambia'),
                   ('GN', 'Guinea'),
                   ('GP', 'Guadeloupe'),
                   ('GQ', 'Equatorial Guinea'),
                   ('GR', 'Greece'),
                   ('GS', 'South Georgia And The South Sandwich Islands'),
                   ('GT', 'Guatemala'),
                   ('GU', 'Guam'),
                   ('GW', 'Guinea-Bissau'),
                   ('GY', 'Guyana'),
                   ('HK', 'Hong Kong'),
                   ('HM', 'Heard And Mc Donald Islands'),
                   ('HN', 'Honduras'),
                   ('HR', 'Croatia (Local Name: Hrvatska)'),
                   ('HT', 'Haiti'),
                   ('HU', 'Hungary'),
                   ('ID', 'Indonesia'),
                   ('IE', 'Ireland'),
                   ('IL', 'Israel'),
                   ('IN', 'India'),
                   ('IO', 'British Indian Ocean Territory'),
                   ('IQ', 'Iraq'),
                   ('IR', 'Iran (Islamic Republic Of)'),
                   ('IS', 'Iceland'),
                   ('IT', 'Italy'),
                   ('JM', 'Jamaica'),
                   ('JO', 'Jordan'),
                   ('JP', 'Japan'),
                   ('KE', 'Kenya'),
                   ('KG', 'Kyrgyzstan'),
                   ('KH', 'Cambodia'),
                   ('KI', 'Kiribati'),
                   ('KM', 'Comoros'),
                   ('KN', 'Saint Kitts And Nevis'),
                   ('KR', 'Korea, Republic Of'),
                   ('KW', 'Kuwait'),
                   ('KY', 'Cayman Islands'),
                   ('KZ', 'Kazakhstan'),
                   ('LA', 'Lao People’s Democratic Republic'),
                   ('LB', 'Lebanon'),
                   ('LC', 'Saint Lucia'),
                   ('LI', 'Liechtenstein'),
                   ('LK', 'Sri Lanka'),
                   ('LR', 'Liberia'),
                   ('LS', 'Lesotho'),
                   ('LT', 'Lithuania'),
                   ('LU', 'Luxembourg'),
                   ('LV', 'Latvia'),
                   ('LY', 'Libyan Arab Jamahiriya'),
                   ('MA', 'Morocco'),
                   ('MC', 'Monaco'),
                   ('MD', 'Moldova, Republic Of'),
                   ('MG', 'Madagascar'),
                   ('MH', 'Marshall Islands'),
                   ('MK', 'Macedonia, The Former Yugoslav Republic Of'),
                   ('ML', 'Mali'),
                   ('MM', 'Myanmar'),
                   ('MN', 'Mongolia'),
                   ('MO', 'Macau'),
                   ('MP', 'Northern Mariana Islands'),
                   ('MQ', 'Martinique'),
                   ('MR', 'Mauritania'),
                   ('MS', 'Montserrat'),
                   ('MT', 'Malta'),
                   ('MU', 'Mauritius'),
                   ('MV', 'Maldives'),
                   ('MW', 'Malawi'),
                   ('MX', 'Mexico'),
                   ('MY', 'Malaysia'),
                   ('MZ', 'Mozambique'),
                   ('NA', 'Namibia'),
                   ('NC', 'New Caledonia'),
                   ('NE', 'Niger'),
                   ('NF', 'Norfolk Island'),
                   ('NG', 'Nigeria'),
                   ('NI', 'Nicaragua'),
                   ('NL', 'Netherlands'),
                   ('NO', 'Norway'),
                   ('NP', 'Nepal'),
                   ('NR', 'Nauru'),
                   ('NU', 'Niue'),
                   ('NZ', 'New Zealand'),
                   ('OM', 'Oman'),
                   ('PA', 'Panama'),
                   ('PE', 'Peru'),
                   ('PF', 'French Polynesia'),
                   ('PG', 'Papua New Guinea'),
                   ('PH', 'Philippines'),
                   ('PK', 'Pakistan'),
                   ('PL', 'Poland'),
                   ('PM', 'St. Pierre And Miquelon'),
                   ('PN', 'Pitcairn'),
                   ('PR', 'Puerto Rico'),
                   ('PS', 'Palestinian Territory, Occupied'),
                   ('PT', 'Portugal'),
                   ('PW', 'Palau'),
                   ('PY', 'Paraguay'),
                   ('QA', 'Qatar'),
                   ('RE', 'Reunion'),
                   ('RO', 'Romania'),
                   ('RS', 'Serbia'),
                   ('RU', 'Russian Federation'),
                   ('RW', 'Rwanda'),
                   ('SA', 'Saudi Arabia'),
                   ('SB', 'Solomon Islands'),
                   ('SC', 'Seychelles'),
                   ('SD', 'Sudan'),
                   ('SE', 'Sweden'),
                   ('SG', 'Singapore'),
                   ('SH', 'St. Helena'),
                   ('SI', 'Slovenia'),
                   ('SJ', 'Svalbard And Jan Mayen Islands'),
                   ('SK', 'Slovakia (Slovak Republic)'),
                   ('SL', 'Sierra Leone'),
                   ('SM', 'San Marino'),
                   ('SN', 'Senegal'),
                   ('SO', 'Somalia'),
                   ('SR', 'Suriname'),
                   ('ST', 'Sao Tome And Principe'),
                   ('SV', 'El Salvador'),
                   ('SZ', 'Swaziland'),
                   ('TC', 'Turks And Caicos Islands'),
                   ('TD', 'Chad'),
                   ('TF', 'French Southern Territories'),
                   ('TG', 'Togo'),
                   ('TH', 'Thailand'),
                   ('TJ', 'Tajikistan'),
                   ('TK', 'Tokelau'),
                   ('TM', 'Turkmenistan'),
                   ('TN', 'Tunisia'),
                   ('TO', 'Tonga'),
                   ('TP', 'East Timor'),
                   ('TR', 'Turkey'),
                   ('TT', 'Trinidad And Tobago'),
                   ('TV', 'Tuvalu'),
                   ('TW', 'Taiwan, Province Of China'),
                   ('TZ', 'Tanzania, United Republic Of'),
                   ('UA', 'Ukraine'),
                   ('UG', 'Uganda'),
                   ('UK', 'United Kingdom'),
                   ('UM', 'United States Minor Outlying Islands'),
                   ('US', 'United States'),
                   ('UY', 'Uruguay'),
                   ('UZ', 'Uzbekistan'),
                   ('VA', 'Holy See (Vatican City State)'),
                   ('VC', 'Saint Vincent And The Grenadines'),
                   ('VE', 'Venezuela'),
                   ('VG', 'Virgin Islands (British)'),
                   ('VI', 'Virgin Islands (U.S.)'),
                   ('VN', 'Viet Nam'),
                   ('VU', 'Vanuatu'),
                   ('WF', 'Wallis And Futuna Islands'),
                   ('WS', 'Samoa'),
                   ('YE', 'Yemen'),
                   ('YT', 'Mayotte'),
                   ('YU', 'Yugoslavia'),
                   ('ZA', 'South Africa'),
                   ('ZM', 'Zambia'),
                   ('ZW', 'Zimbabwe'),
                   ('IM', 'Isle Of Man'),
                   ('AX', 'Åland Islands'),
                   ('BL', 'Saint Barthélemy'),
                   ('BQ', 'Bonaire, Sint Eustatius and Saba'),
                   ('GG', 'Guernsey'),
                   ('JE', 'Jersey'),
                   ('ME', 'Montenegro'),
                   ('MF', 'Saint Martin'),
                   ('SS', 'South Sudan'),
                   ('SX', 'Sint Maarten'),
                   ('TL', 'East Timor'),
                   ('AB', 'Abkhazia'),
                   ('XK', 'Kosovo')]

game_choices = [('game_shows', 'Game Shows'),
                ('baccarat_sicbo', 'Baccarat'),
                ('poker', 'Poker'),
                ('top_games', 'Top Games'),
                ('roulette', 'Roulette'),
                ('blackjack', 'Blackjack'),
                ('reward_games', 'Reward Games'),
                ('slots', 'Slots')]


class OneWalletAddUser(FlaskForm):
    # sid = StringField('sid', validators=[InputRequired()])
    # uuid = StringField('uuid', validators=[InputRequired()])
    userID_added = StringField('userID', validators=[InputRequired()])
    balance = StringField('Starting balance', validators=[InputRequired()])
    add_userid = SubmitField('Add')


class OneWalletFindUser(FlaskForm):
    # sid = StringField('sid', validators=[InputRequired()])
    # uuid = StringField('uuid', validators=[InputRequired()])
    userID = StringField('Player ID', validators=[InputRequired()])
    find_userid = SubmitField('Find')


class FundTransferForm(FlaskForm):
    amount = StringField('Amount', validators=[InputRequired()])
    add = SubmitField('+')
    subtract = SubmitField('-')


class UserAuthenticationForm(FlaskForm):
    firstName = StringField('First Name', validators=[InputRequired()])
    lastName = StringField('Last Name', validators=[InputRequired()])
    nickname = StringField('Nickname', validators=[InputRequired()])
    country = SelectField('Country', choices=country_choices)
    language = SelectField('Language', choices=language_choices)
    game = SelectField('Game Category', choices=game_choices)
    update = SubmitField('Update')
