/* ── HM WATCHES — Shared Inventory Data ──────────────────────────────────
   Replace this with a Supabase/API fetch when the backend is ready.
   Pexels images are free for commercial use (pexels.com/license).
   ──────────────────────────────────────────────────────────────────────── */
const WATCHES = [
  {
    id: 1,
    brand: "Richard Mille",
    model: "RM 67-02",
    ref: "RM 67-02",
    year: 2022,
    case_material: "Carbon TPT",
    case_size: "38.7 × 47.5 mm",
    dial: "Skeletonized",
    movement: "Manual winding, CRMA7 caliber",
    condition: "Excellent",
    papers: true,
    box: true,
    price: 195000,
    currency: "USD",
    status: "available",
    description: "The RM 67-02 represents the pinnacle of Richard Mille's ultra-light philosophy. Crafted from Carbon TPT — a material developed for Formula 1 — the case weighs under 40 grams complete. The skeletonized movement is suspended in a baseplate and bridges also made from Carbon TPT, revealing the full architecture of the caliber CRMA7.",
    photos: [
      "https://images.pexels.com/photos/5058216/pexels-photo-5058216.jpeg?auto=compress&cs=tinysrgb&w=900",
      "https://images.pexels.com/photos/3419331/pexels-photo-3419331.jpeg?auto=compress&cs=tinysrgb&w=900",
      "https://images.pexels.com/photos/9267843/pexels-photo-9267843.jpeg?auto=compress&cs=tinysrgb&w=900"
    ]
  },
  {
    id: 2,
    brand: "Rolex",
    model: "Daytona",
    ref: "116500LN",
    year: 2021,
    case_material: "Oystersteel",
    case_size: "40 mm",
    dial: "Black, Chronograph",
    movement: "Automatic, Caliber 4130",
    condition: "Mint",
    papers: true,
    box: true,
    price: 38000,
    currency: "USD",
    status: "available",
    description: "Reference 116500LN is the steel Daytona with black ceramic bezel — one of the most sought-after sports watches of the modern era. Powered by the in-house Caliber 4130 with a 72-hour power reserve. This example is in mint condition with full set.",
    photos: [
      "https://images.pexels.com/photos/364822/rolex-watch-time-luxury-364822.jpeg?auto=compress&cs=tinysrgb&w=900",
      "https://images.pexels.com/photos/190819/pexels-photo-190819.jpeg?auto=compress&cs=tinysrgb&w=900",
      "https://images.pexels.com/photos/380782/pexels-photo-380782.jpeg?auto=compress&cs=tinysrgb&w=900"
    ]
  },
  {
    id: 3,
    brand: "Audemars Piguet",
    model: "Royal Oak",
    ref: "15500ST.OO.1220ST.01",
    year: 2023,
    case_material: "Stainless Steel",
    case_size: "41 mm",
    dial: "Blue",
    movement: "Automatic, Caliber 4302",
    condition: "Like New",
    papers: true,
    box: true,
    price: 58000,
    currency: "USD",
    status: "available",
    description: "The 41mm Royal Oak ref. 15500ST is the definitive modern interpretation of Gérald Genta's 1972 icon. The blue Grande Tapisserie dial is framed by the signature octagonal bezel secured with eight hexagonal screws. Powered by the ultra-thin Caliber 4302 with 70-hour power reserve.",
    photos: [
      "https://images.pexels.com/photos/3419331/pexels-photo-3419331.jpeg?auto=compress&cs=tinysrgb&w=900",
      "https://images.pexels.com/photos/9267843/pexels-photo-9267843.jpeg?auto=compress&cs=tinysrgb&w=900"
    ]
  },
  {
    id: 4,
    brand: "Patek Philippe",
    model: "Nautilus",
    ref: "5711/1A-010",
    year: 2020,
    case_material: "Stainless Steel",
    case_size: "40 mm",
    dial: "Blue Sunburst",
    movement: "Automatic, Caliber 26-330 S C",
    condition: "Very Good",
    papers: true,
    box: false,
    price: 145000,
    currency: "USD",
    status: "sold",
    description: "Reference 5711/1A in steel with the iconic blue sunburst dial — one of the most coveted references in all of watchmaking. Discontinued in 2021, demand for this reference has never been stronger. This 2020 example is accompanied by its original Patek Philippe papers.",
    photos: [
      "https://images.pexels.com/photos/60147/pexels-photo-60147.jpeg?auto=compress&cs=tinysrgb&w=900",
      "https://images.pexels.com/photos/3809175/pexels-photo-3809175.jpeg?auto=compress&cs=tinysrgb&w=900"
    ]
  },
  {
    id: 5,
    brand: "Rolex",
    model: "Submariner",
    ref: "126610LN",
    year: 2022,
    case_material: "Oystersteel",
    case_size: "41 mm",
    dial: "Black",
    movement: "Automatic, Caliber 3235",
    condition: "Excellent",
    papers: true,
    box: true,
    price: 18500,
    currency: "USD",
    status: "available",
    description: "The 126610LN is the current-generation Submariner in steel with black dial and Cerachrom ceramic bezel. Updated to 41mm in 2020, it houses the Caliber 3235 with 70-hour power reserve. Full set, recently serviced by an authorised Rolex service centre.",
    photos: [
      "https://images.pexels.com/photos/190819/pexels-photo-190819.jpeg?auto=compress&cs=tinysrgb&w=900",
      "https://images.pexels.com/photos/380782/pexels-photo-380782.jpeg?auto=compress&cs=tinysrgb&w=900"
    ]
  },
  {
    id: 6,
    brand: "Audemars Piguet",
    model: "Royal Oak Offshore",
    ref: "26400RO.OO.A002CA.01",
    year: 2019,
    case_material: "18k Rose Gold",
    case_size: "44 mm",
    dial: "Slate Grey",
    movement: "Automatic Chronograph, Caliber 3126/3840",
    condition: "Very Good",
    papers: true,
    box: true,
    price: 88000,
    currency: "USD",
    status: "available",
    description: "The Royal Oak Offshore 44mm in 18k rose gold with slate grey dial. Bold, architectural, unmistakable. The chronograph pushers and crown are protected by the signature rubber-coated crown guards. Complete with original AP box and papers.",
    photos: [
      "https://images.pexels.com/photos/16739804/pexels-photo-16739804.jpeg?auto=compress&cs=tinysrgb&w=900",
      "https://images.pexels.com/photos/5058216/pexels-photo-5058216.jpeg?auto=compress&cs=tinysrgb&w=900"
    ]
  }
];

if (typeof module !== "undefined") module.exports = WATCHES;
