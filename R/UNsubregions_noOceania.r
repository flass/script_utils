#!/usr/bin/env R
subregions = list(
`Northern Africa`=c('Algeria', 'Egypt', 'Libya', 'Morocco', 'Sudan', 'Tunisia', 'Western Sahara'),

`Eastern Africa`=c('British Indian Ocean Territory', 'Burundi', 'Comoros', 'Djibouti', 'Eritrea', 'Ethiopia', 'French Southern Territories', 'Kenya', 'Madagascar', 'Malawi', 'Mauritius', 'Mayotte', 'Mozambique', 'Réunion', 'Rwanda', 'Seychelles', 'Somalia', 'South Sudan', 'Uganda', 'United Republic of Tanzania', 'Zambia', 'Zimbabwe'),

`Middle Africa`=c('Angola', 'Cameroon', 'Central African Republic', 'Chad', 'Congo', 'Democratic Republic of the Congo', 'Equatorial Guinea', 'Gabon', 'Sao Tome and Principe'),

`Southern Africa`=c('Botswana', 'Eswatini', 'Lesotho', 'Namibia', 'South Africa'),

`Western Africa`=c('Benin', 'Burkina Faso', 'Cabo Verde', 'Côte d\'Ivoire', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Liberia', 'Mali', 'Mauritania', 'Niger', 'Nigeria', 'Saint Helena', 'Senegal', 'Sierra Leone', 'Togo'),

`Caribbean`=c('Anguilla', 'Antigua and Barbuda', 'Aruba', 'Bahamas', 'Barbados', 'Bonaire, Sint Eustatius and Saba', 'British Virgin Islands', 'Cayman Islands', 'Cuba', 'Curaçao', 'Dominica', 'Dominican Republic', 'Grenada', 'Guadeloupe', 'Haiti', 'Jamaica', 'Martinique', 'Montserrat', 'Puerto Rico', 'Saint Barthélemy', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin', 'Saint Vincent and the Grenadines', 'Sint Maarten', 'Trinidad and Tobago', 'Turks and Caicos Islands', 'United States Virgin Islands'),

`Central America`=c('Belize', 'Costa Rica', 'El Salvador', 'Guatemala', 'Honduras', 'Mexico', 'Nicaragua', 'Panama'),

`South America`=c('Argentina', 'Bolivia', 'Bouvet Island', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Falkland Islands', 'French Guiana', 'Guyana', 'Paraguay', 'Peru', 'South Georgia and the South Sandwich Islands', 'Suriname', 'Uruguay', 'Venezuela'),

`Northern America`=c('Bermuda', 'Canada', 'Greenland', 'Saint Pierre and Miquelon', 'United States of America'),

`Central Asia`=c('Kazakhstan', 'Kyrgyzstan', 'Tajikistan', 'Turkmenistan', 'Uzbekistan'),

`Eastern Asia`=c('China', 'Hong Kong', 'Macao', 'Democratic People\'s Republic of Korea', 'Japan', 'Mongolia', 'Republic of Korea', 'Taiwan'),

`South-eastern Asia`=c('Brunei Darussalam', 'Cambodia', 'Indonesia', 'Lao People\'s Democratic Republic', 'Malaysia', 'Myanmar', 'Philippines', 'Singapore', 'Thailand', 'Timor-Leste', 'Viet Nam'),

`Southern Asia`=c('Afghanistan', 'Bangladesh', 'Bhutan', 'India', 'Iran (Islamic Republic of)', 'Maldives', '  Nepal', 'Pakistan', 'Sri Lanka'),

`Western Asia`=c('Armenia', 'Azerbaijan', 'Bahrain', 'Cyprus', 'Georgia', 'Iraq', 'Israel', 'Jordan', 'Kuwait', 'Lebanon', 'Oman', 'Qatar', 'Saudi Arabia', 'State of Palestine', 'Syrian Arab Republic', 'Turkey', 'United Arab Emirates', 'Yemen'),

`Eastern Europe`=c('Belarus', 'Bulgaria', 'Czechia', 'Hungary', 'Poland', 'Republic of Moldova', 'Romania', 'Russian Federation', 'Slovakia', 'Ukraine'),

`Northern Europe`=c('Åland Islands', 'Channel Islands', 'Guernsey', 'Jersey', 'Sark', 'Denmark', 'Estonia', 'Faroe Islands', 'Finland', 'Iceland', 'Ireland', 'Isle of Man', 'Latvia', 'Lithuania', 'Norway', 'Svalbard and Jan Mayen Islands', 'Sweden', 'United Kingdom of Great Britain and Northern Ireland'),

`Southern Europe`=c('Albania', 'Andorra', 'Bosnia and Herzegovina', 'Croatia', 'Gibraltar', 'Greece', 'Holy See', 'Italy', 'Malta', 'Montenegro', 'North Macedonia', 'Portugal', 'San Marino', 'Serbia', 'Slovenia', 'Spain'),

`Western Europe`=c('Austria', 'Belgium', 'France', 'Germany', 'Liechtenstein', 'Luxembourg', 'Monaco', 'Netherlands', 'Switzerland')
)

continents = list(
Africa=c("Northern Africa", "Eastern Africa", "Middle Africa", "Southern Africa", "Western Africa"),
America=c("Caribbean", "Central America", "South America", "Northern America"),
Asia=c("Central Asia", "Eastern Asia", "South-eastern Asia", "Southern Asia", "Western Asia"),
Europe=c("Eastern Europe", "Northern Europe", "Southern Europe", "Western Europe")
)