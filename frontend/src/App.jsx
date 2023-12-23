import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './App.css';

import L from 'leaflet';

const customIcon = new L.Icon({
    iconUrl: './zus.png',
    iconSize: [25, 25],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    tooltipAnchor: [16, -28],
});

const malaysiaCenter = [4.2105, 107.9758]; // Latitude and longitude for Malaysia
const defaultZoom = 6;

export default function App() {
    const [stores, setStores] = useState([]);
    const [selectedMarker, setSelectedMarker] = useState(null);

    useEffect(() => {
        // Fetch store details from my backend FastAPI endpoint
        fetch('http://127.0.0.1:8000/stores')
            .then(response => response.json())
            .then((res) => {
                console.log(res);
                setStores(res);
            })
            .catch(error => console.error('Error fetching store details:', error));
    }, []); 

    const calculateCircle = (latitude, longtitude) => {
        return (
            <Circle
                center={[latitude, longtitude]}
                radius={5000} // 5KM radius
                color="blue"
                fillColor="blue"
                fillOpacity={0.1}
            />
        );
    };

    const handleMarkerClick = (markerId) => {
        console.log(markerId,"here here")  
        setSelectedMarker(markerId === selectedMarker ? null : markerId);
    };

    return (
        <div className="App">
            <h1>Geocoding Web Application</h1>
            <MapContainer center={malaysiaCenter} zoom={defaultZoom} style={{ height: '400px', width: '100%' }}>
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {stores.map(store => (
                    <React.Fragment key={store.id}>
                        <Marker
                            position={[store.latitude, store.longtitude]}
                            icon={customIcon}
                            eventHandlers={{
                                click: () => {
                                    console.log('Marker clicked:', store.id);
                                    handleMarkerClick(store.id);
                                },
                            }}
                        >
                            <Popup>
                                <div>
                                    <h2>{store.name}</h2>
                                    <p>{store.address}</p>
                                </div>
                            </Popup>
                        </Marker>
                        {selectedMarker === store.id && calculateCircle(store.latitude, store.longtitude)}
                    </React.Fragment>
                ))}
            </MapContainer>
        </div>
    );
}