// Demo prose for the website screenshots. Original text in the spirit of
// Mary Shelley's Frankenstein (the seed's Story Bible), plus one Spanish book.
// US spelling on purpose: the bundled English dictionary is en_US.

export const CHAPTERS = [
  {
    title: 'Letter I',
    synopsis: 'Walton writes to his sister from St. Petersburg, restless to sail north and find the passage no one has found.',
    label: 'blue', status: 'done',
    body: `You will rejoice to hear that no disaster has accompanied the beginning of an enterprise which you have regarded with such evil forebodings. I arrived here yesterday, and my first task is to assure my dear sister of my welfare.

I am already far north of London, and as I walk in the streets of the city I feel a cold northern breeze play upon my cheeks, which braces my nerves and fills me with delight. This breeze, which has traveled from the regions toward which I am advancing, gives me a foretaste of those icy climes.

I try in vain to be persuaded that the pole is the seat of frost and desolation. It ever presents itself to my imagination as the region of beauty and delight. There, Margaret, the sun is forever visible, its broad disk just skirting the horizon and diffusing a perpetual splendor.

You may deem me romantic, my dear sister, but I bitterly feel the want of a friend. I have no one near me, gentle yet courageous, whose eyes would reply to mine.`,
  },
  {
    title: 'By the Lake',
    synopsis: "Victor's childhood by the lake. Elizabeth arrives, and the family closes around her like a hand.",
    label: 'red', status: 'revised',
    body: `I was born in Geneva, and my family is one of the most distinguished of that republic. My father had filled several public situations with honor and reputation, and he was respected by all who knew him for his integrity and his patience with public business.

No human being could have passed a happier childhood than myself. My parents were possessed by the very spirit of kindness and indulgence. We lived in a house by the lake, and in the summer evenings we rowed out until the mountains turned violet and the water held the last of the light.

When I was four years old, my mother brought home a little girl with hair the color of gold. Her name was Elizabeth. She was gentle where I was fierce, patient where I was impatient, and from that evening she was my more than sister.

I delighted in investigating the facts relative to the actual world; she busied herself with following the aerial creations of the poets. We were strangers to any species of disunion or dispute.`,
  },
  {
    title: 'The University',
    synopsis: 'At the university Victor abandons the ancient alchemists for modern chemistry, and an obsession takes root.',
    label: 'red', status: 'revised',
    body: `The professor began his lecture with a recapitulation of the history of chemistry. He spoke of the ancient masters, who promised impossibilities and performed nothing, and of the modern masters, who promise very little and yet perform miracles.

Such were the professor's words, rather let me say such the words of fate, spoken to destroy me. As he went on I felt as if my soul were grappling with a palpable enemy; one by one the various keys were touched which formed the mechanism of my being.

From this day natural philosophy, and particularly chemistry, became nearly my sole occupation. I read with ardor the works of the new masters. I attended the lectures, and I cultivated the acquaintance of the men of science of the university.

Two years passed in this manner, during which I paid no visit to Geneva. My application was so ardent that I often saw the stars disappear in the light of morning while I was yet engaged in my laboratory.`,
  },
  {
    title: 'The Spark',
    synopsis: 'On a dreary November night the creature opens its eyes, and Victor flees from what he has made.',
    label: 'red', status: 'draft',
    body: `It was on a dreary night of November that I beheld the accomplishment of my toils. With an anxiety that almost amounted to agony, I collected the instruments of life around me, that I might infuse a spark of being into the lifeless thing that lay at my feet.

It was already one in the morning; the rain pattered dismally against the panes, and my candle was nearly burnt out, when, by the glimmer of the half-extinguished light, I saw the dull yellow eye of the creature open. It breathed hard, and a convulsive motion agitated its limbs.

How can I describe my emotions at this catastrophe? I had worked hard for nearly two years, for the sole purpose of infusing life into an inanimate body. Now that I had finished, the beauty of the dream vanished, and breathless horror and disgust filled my heart.

Unable to endure the aspect of the being I had created, I rushed out of the room and paced my bedchamber for a long time, unable to compose my mind to sleep.`,
  },
  {
    title: 'The Hovel',
    synopsis: 'Hidden beside a cottage, the creature watches the De Lacey family through a chink in the wall and learns to speak.',
    label: 'purple', status: 'draft',
    body: `It is with considerable difficulty that I remember the original era of my being. A strange multiplicity of sensations seized me, and I saw, felt, heard, and smelt at the same time.

I found a low hovel against the wall of a cottage, and there I made my home. Through a small chink in the boards I could see into the room beyond: an old man playing upon an instrument, a young girl at her work, a youth who came in each evening with wood for the fire.

By degrees I made a discovery of still greater moment. I found that these people possessed a method of communicating their experience and feelings to one another by articulate sounds. This was indeed a godlike science, and I ardently desired to become acquainted with it.

I learned the words fire, milk, bread, and wood. I learned the names of the cottagers themselves. And I learned, at last, what I was.`,
  },
  {
    title: 'The Ice',
    synopsis: "Walton's ship is locked in the ice. A stranger on a sledge is pulled aboard, half frozen and wholly changed.",
    label: 'blue', status: 'outline',
    body: `Last Monday we were nearly surrounded by ice, which closed in the ship on all sides, scarcely leaving her the sea room in which she floated. A strange sight suddenly attracted our attention.

We perceived a low carriage, fixed on a sledge and drawn by dogs, pass on toward the north, at the distance of half a mile. A being which had the shape of a man, but apparently of gigantic stature, sat in the sledge and guided the dogs.

In the morning we found a second sledge drifting beside us on a fragment of ice, and in it a man, nearly frozen, whom we brought aboard. I never saw a man in so wretched a condition.`,
  },
];

// Written to trip every analysis: repeated words, adverbs, gerunds, adjectives,
// same openings, a run of equal-length sentences, and end rhymes.
export const ROUGH = {
  title: 'The Spark (rough draft)',
  synopsis: 'First pass at the creation night. Needs cutting.',
  label: 'orange', status: 'draft',
  body: `It was a dark night in November. The rain fell hard on the glass. The candle burned low in its dish. The room was cold and very still. He looked at the thing on the table. He held the instruments carefully and nervously. He waited quietly for the spark. He have waited for two long years, waiting and hoping and working through every endless night, and now the night was finally here, and the night would not wait for him.

Slowly, the yellow eye opened. Trembling, Victor stepped back from the table, staring at the dull and watery eye, the yellow skin, the long black hair. The light was bright, the sight was white, and he ran from the room into the night.

He walked quickly through the empty streets. He did not look back. He could not bear to look back at the thing he had made, the thing he had made with his own hands, the thing he had always dreamed of making.`,
};

// The Spark's earlier wording, kept as a snapshot so the diff has something to show.
export const SPARK_FIRST_DRAFT = `It was on a dark and stormy night of November that I saw the end of my work. With great anxiety I gathered the instruments of life around me, so that I could put a spark of being into the thing that lay at my feet.

It was already one in the morning; the rain beat against the windows, and my candle was nearly gone, when, by the last of the light, I saw the yellow eye of the creature open. It breathed, and its limbs moved.

How can I describe my emotions at this catastrophe? I had worked hard for nearly two years, for the sole purpose of infusing life into an inanimate body. Now that I had finished, the dream was gone, and horror filled my heart.

I could not stand to look at it, so I ran out of the room and walked up and down my bedroom for hours.`;

export const SPANISH = {
  name: 'El faro de Arnela',
  chapters: [
    {
      title: 'I. La llegada',
      synopsis: 'Inés llega a la isla en el último barco del otoño para hacerse cargo del faro.',
      label: 'blue', status: 'revised',
      body: `El barco del correo la dejó en el muelle a media tarde, cuando la marea empezaba a bajar y las gaviotas ya se habían cansado de seguirlo. Inés bajó con una maleta de cartón y una caja de libros atada con cuerda, y nadie salió a recibirla.

El pueblo eran doce casas de piedra apretadas contra la ladera, como si el viento las hubiera empujado hasta allí. Arriba, en el extremo de la isla, el faro esperaba blanco y callado, con la linterna apagada.

Subió el camino despacio. Le habían dicho que el antiguo farero se había marchado sin despedirse, que una mañana el bote ya no estaba en la playa y que nadie volvió a saber de él. Le habían dicho también que no hiciera preguntas.

Cuando llegó a la puerta, la llave estaba puesta en la cerradura. Dentro olía a petróleo y a sal, y sobre la mesa de la cocina había una taza todavía tibia.`,
    },
    {
      title: 'II. El cuaderno',
      synopsis: 'En el cuarto de la linterna Inés encuentra el diario del farero, interrumpido a mitad de una frase.',
      label: 'blue', status: 'draft',
      body: `El cuaderno estaba debajo del banco de trabajo, envuelto en un hule. Las primeras páginas hablaban del tiempo, de los barcos que pasaban, del precio del aceite. Las últimas hablaban de una luz en el mar que no era de ningún barco.`,
    },
    {
      title: 'III. La tormenta',
      synopsis: 'La primera tormenta del invierno deja la isla incomunicada.',
      label: 'red', status: 'outline',
      body: `La tormenta llegó de noche, sin avisar.`,
    },
  ],
};
