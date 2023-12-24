import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './App.css';
import { calculateDistance } from './utils';

import L from 'leaflet';

//icon components
const customIcon = new L.Icon({
    iconUrl: './zus.png',
    iconSize: [25, 25],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    tooltipAnchor: [16, -28],
});

//highlighted icon components
const highlightedIcon = new L.Icon({
    iconUrl: './latte.png', 
    iconSize: [23, 39],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    tooltipAnchor: [16, -28],
});

const malaysiaCenter = [4.2105, 107.9758]; // Latitude and longtitude for Malaysia
const defaultZoom = 6;

export default function App() {
    const [stores, setStores] = useState([]);
    const [selectedMarker, setSelectedMarker] = useState(null);
    const [highlightedStores, setHighlightedStores] = useState([]);

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

    useEffect(() => {
        // Update highlighted stores when selectedMarker changes
        if (selectedMarker !== null) {
            const selectedStore = stores.find(store => store.id === selectedMarker);
            if (selectedStore) {
                const highlightedStores = stores.filter(store =>
                    calculateDistance(store.latitude, store.longtitude, selectedStore.latitude, selectedStore.longtitude) <= 5000
                );
                setHighlightedStores(highlightedStores.map(store => store.id));
            }
        }
    }, [selectedMarker, stores]);

    const calculateCircle = (latitude, longitude) => {
        return (
            <Circle
                center={[latitude, longitude]}
                radius={5000} // 5KM radius
                color="blue"
                fillColor="blue"
                fillOpacity={0.1}
            />
        );
    };

    //fucntion to handle marker click
    const handleMarkerClick = (markerId) => {
        setSelectedMarker(markerId === selectedMarker ? null : markerId);
    };

    const storesWithHighlight = stores.map(store => ({
        ...store,
        isWithinRadius: highlightedStores.includes(store.id),
    }));


    return (
        <div className="App">
            <h1>Geocoding Web Application</h1>
            <MapContainer center={malaysiaCenter} zoom={defaultZoom} style={{ height: '400px', width: '100%' }}>
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {storesWithHighlight.map(store => (
                    <React.Fragment key={store.id}>
                        <Marker
                            position={[store.latitude, store.longtitude]}
                            icon={store.isWithinRadius ? highlightedIcon : customIcon}
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
                    </React.Fragment>
                ))}
                {selectedMarker !== null &&
                    calculateCircle(
                        stores.find(store => store.id === selectedMarker).latitude,
                        stores.find(store => store.id === selectedMarker).longtitude
                    )}
            </MapContainer>
        </div>
    );
}