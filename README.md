# NFL Fantasy Dashboard – Power BI  

## Project Overview  
This project is an interactive Power BI dashboard analyzing NFL fantasy football data across players, positions, and teams. The goal was to uncover key trends in player usage, scoring efficiency, and team-level target distribution to support data-driven decision-making for fantasy football managers.  

---

## Data Source  
Data was collected from FantasyPros, combining player- and team-level statistics including:  
- Player information: name, position, team, bye week  
- Fantasy projections (PPR format) and average draft position (ADP)  
- Historical performance metrics (2024 season)  
- Advanced usage metrics: team target share, red-zone opportunities, snap counts  

The final dataset included 400+ players/fantasy entities across all NFL teams.  

---

## Key Insights  
- **WR Target % Top 5:** Los Angeles Rams (74.5%), New York Giants (72.6%), Chicago Bears (72.1%), Indianapolis Colts (71.5%), Atlanta Falcons (68.1%)  
  *Insight:* Identifies wide receivers likely to receive more targets, translating into higher fantasy opportunities.  

- **RB Target % Top 5:** New Orleans Saints (26.1%), Pittsburgh Steelers (23.7%), Miami Dolphins (23.1%), Tampa Bay Buccaneers (21.5%), Denver Broncos (21.4%)  
  *Insight:* Valuable for PPR leagues, as higher target percentages boost reception-based points for running backs.  

- **TE Target % Top 5:** Arizona Cardinals (34%), Kansas City Chiefs (33.7%), Las Vegas Raiders (33.5%), New England Patriots (31.9%), Baltimore Ravens (30.2%)  
  *Insight:* Shows which tight ends are likely to get more targets, providing clear guidance for fantasy lineup decisions.  

- **Digestibility for All Users:** Multi-card visuals include player rankings and key metrics, making it easy for fantasy players—regardless of data familiarity—to quickly compare performance and projections.  

---

## Interactive Features  
- **Player Selection Multi-Cards:** Select a player to highlight their ADP, position rank, projected points, target share, and see them highlighted across scatter plots.  
- **Team Target Share Multi-Cards:** On the overview page, select a team to highlight all players’ performance and usage metrics.  
- **Scatter Plots:** Clicking on a player pulls up their performance and projections for the year, enabling interactive comparisons.  
- **Navigation & Search:** Vertical navigation bar, search slicer by player, and direct links to ESPN Fantasy and Yahoo Fantasy live draft projections.  

---

## Tools & Methods  
- **Python** – Web scraping from FantasyPros, data extraction, cleaning, and preparation  
- **Power BI Desktop** – Data modeling, DAX calculations, multi-card visuals, and interactive dashboard creation  
- **Excel/CSV** – Base data storage, validation, and preprocessing  

---


## Skills Highlight  
- Built an end-to-end ETL pipeline: scraped and extracted raw data, cleaned and transformed it into analysis-ready datasets, and loaded it into Power BI.
- Created **DAX measures** for usage metrics (e.g., target share, red-zone efficiency)
- Designed interactive multi-card visuals and scatter plots for intuitive player and team comparison.  
- Converted raw player statistics into actionable fantasy football insights through formatted multi-card visuals and scatter plots, enabling clear evaluation of player usage, efficiency, and projected scoring.  

---

## Dashboard Preview
![Dashboard Screenshot](dashboard_overview_page.PNG)

## Positional Preview
![QB Overview Screenshot](qb_overview_page.PNG)
![RB Overview Screenshot](rb_overview_page.PNG)
![WR Overview Screenshot](wr_overview_page.PNG)
![TE Overview Screenshot](te_overview_page.PNG)
![K Overview Screenshot](k_overview_page.PNG)
![DST Overview Screenshot](dst_overview_page.PNG)
