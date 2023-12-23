import React, { useEffect, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './App.css';

const outlets = [
    { id: 1, name: 'Outlet 1', lat: 40.7128, lon: -74.0060 },
    { id: 2, name: 'Outlet 2', lat: 34.0522, lon: -118.2437 },
    // Add more outlet data as needed
];

export default function App() {
    const [map, setMap] = useState(null);

    useEffect(() => {
        // Initialize Leaflet map
        const leafletMap = L.map('map').setView([0, 0], 2);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(leafletMap);
        setMap(leafletMap);

        return () => {
            // Clean up resources, e.g., remove the map instance
            leafletMap.remove();
        };
    }, []); // Empty dependency array ensures this effect runs only once

    useEffect(() => {
        if (map) {
            outlets.forEach(outlet => {
                // Draw circle with 5KM radius around each outlet
                const circle = L.circle([outlet.lat, outlet.lon], {
                    color: 'blue',
                    fillColor: 'blue',
                    fillOpacity: 0.2,
                    radius: 5000
                }).addTo(map);

                // TODO: Highlight or mark outlets that intersect
            });
        }
    }, [map]);

    return (
        <div className="App">
            <div id="map" className="map"></div>
        </div>
    );
}