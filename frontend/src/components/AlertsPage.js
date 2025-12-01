import React, { useState } from 'react';
import { useLanguage } from '../context/LanguageContext';
import { mockAlerts, mockGoldPrices, mockCurrencies } from '../mock';
import { Plus, Bell, BellOff, Trash2 } from 'lucide-react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Switch } from './ui/switch';

const AlertsPage = () => {
  const { t, language } = useLanguage();
  const [alerts, setAlerts] = useState(mockAlerts);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [newAlert, setNewAlert] = useState({
    itemName: '',
    targetPrice: '',
    condition: 'above'
  });

  const allItems = [
    ...mockGoldPrices.map(item => ({
      value: language === 'tr' ? item.name : item.nameEn,
      label: language === 'tr' ? item.name : item.nameEn,
      currentPrice: item.sell,
      nameEn: item.nameEn
    })),
    ...mockCurrencies.map(item => ({
      value: language === 'tr' ? item.name : item.nameEn,
      label: language === 'tr' ? item.name : item.nameEn,
      currentPrice: item.sell,
      nameEn: item.nameEn
    }))
  ];

  const handleAddAlert = () => {
    if (newAlert.itemName && newAlert.targetPrice) {
      const selectedItem = allItems.find(item => item.value === newAlert.itemName);
      const alert = {
        id: Date.now(),
        itemName: newAlert.itemName,
        itemNameEn: selectedItem?.nameEn || newAlert.itemName,
        targetPrice: parseFloat(newAlert.targetPrice),
        currentPrice: selectedItem?.currentPrice || 0,
        condition: newAlert.condition,
        active: true
      };
      setAlerts([...alerts, alert]);
      setNewAlert({ itemName: '', targetPrice: '', condition: 'above' });
      setIsDialogOpen(false);
    }
  };

  const handleDeleteAlert = (id) => {
    setAlerts(alerts.filter(alert => alert.id !== id));
  };

  const handleToggleAlert = (id) => {
    setAlerts(alerts.map(alert => 
      alert.id === id ? { ...alert, active: !alert.active } : alert
    ));
  };

  return (
    <div className="pb-20 pt-6 px-4">
      <div className="max-w-md mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-yellow-600 font-bold text-lg">{t('alerts_title')}</h2>
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button className="bg-yellow-500 hover:bg-yellow-600 text-white">
                <Plus size={18} className="mr-1" />
                {t('add_alert')}
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-sm">
              <DialogHeader>
                <DialogTitle>{t('add_alert')}</DialogTitle>
              </DialogHeader>
              <div className="space-y-4 mt-4">
                <div>
                  <Label>{t('selectItem')}</Label>
                  <select
                    value={newAlert.itemName}
                    onChange={(e) => setNewAlert({ ...newAlert, itemName: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg mt-1"
                  >
                    <option value="">{t('selectItem')}</option>
                    {allItems.map(item => (
                      <option key={item.value} value={item.value}>
                        {item.label}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <Label>{t('target_price')}</Label>
                  <Input
                    type="number"
                    value={newAlert.targetPrice}
                    onChange={(e) => setNewAlert({ ...newAlert, targetPrice: e.target.value })}
                    placeholder="0.00"
                    className="mt-1"
                  />
                </div>
                <div>
                  <Label>{t('condition')}</Label>
                  <select
                    value={newAlert.condition}
                    onChange={(e) => setNewAlert({ ...newAlert, condition: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg mt-1"
                  >
                    <option value="above">{t('above')}</option>
                    <option value="below">{t('below')}</option>
                  </select>
                </div>
                <div className="flex gap-2">
                  <Button onClick={() => setIsDialogOpen(false)} variant="outline" className="flex-1">
                    {t('cancel')}
                  </Button>
                  <Button onClick={handleAddAlert} className="flex-1 bg-yellow-500 hover:bg-yellow-600">
                    {t('save')}
                  </Button>
                </div>
              </div>
            </DialogContent>
          </Dialog>
        </div>

        {/* Alerts List */}
        {alerts.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            <Bell size={48} className="mx-auto mb-3 opacity-30" />
            <p>{t('alerts_empty')}</p>
          </div>
        ) : (
          <div className="space-y-3">
            {alerts.map((alert) => {
              const name = language === 'tr' ? alert.itemName : alert.itemNameEn;
              const isTriggered = 
                (alert.condition === 'above' && alert.currentPrice >= alert.targetPrice) ||
                (alert.condition === 'below' && alert.currentPrice <= alert.targetPrice);
              
              return (
                <div 
                  key={alert.id} 
                  className={`bg-white border rounded-lg p-4 shadow-sm transition-all ${
                    isTriggered && alert.active ? 'border-yellow-400 bg-yellow-50' : 'border-gray-200'
                  }`}
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-3">
                      {alert.active ? (
                        <Bell size={20} className="text-yellow-600" />
                      ) : (
                        <BellOff size={20} className="text-gray-400" />
                      )}
                      <div>
                        <h3 className="font-bold text-gray-800">{name}</h3>
                        <p className="text-xs text-gray-500">
                          {alert.condition === 'above' ? t('above') : t('below')} {alert.targetPrice.toLocaleString('tr-TR', { minimumFractionDigits: 2 })} ₺
                        </p>
                      </div>
                    </div>
                    <button
                      onClick={() => handleDeleteAlert(alert.id)}
                      className="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                  
                  <div className="flex items-center justify-between pt-3 border-t">
                    <div>
                      <p className="text-xs text-gray-500">Güncel Fiyat</p>
                      <p className="font-bold text-gray-800">
                        {alert.currentPrice.toLocaleString('tr-TR', { minimumFractionDigits: 2 })} ₺
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-sm text-gray-600">
                        {alert.active ? t('active') : t('inactive')}
                      </span>
                      <Switch
                        checked={alert.active}
                        onCheckedChange={() => handleToggleAlert(alert.id)}
                      />
                    </div>
                  </div>

                  {isTriggered && alert.active && (
                    <div className="mt-3 p-2 bg-yellow-100 rounded text-xs font-semibold text-yellow-800 text-center">
                      ⚠️ Hedef fiyata ulaşıldı!
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default AlertsPage;