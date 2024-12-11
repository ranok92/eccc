years = 2015:5:2055;
figure

for k =1:8
year = years(k);

% data = readtable( sprintf('./Results/withEV%d.xlsx', year) );
data = readtable( sprintf('./Results_backup/nonEV%d.xlsx', year) );

for t =1:5
subplot(2,3,t)

plot(0:23, data{t,4:end}*data{t,3}/100, 'DisplayName', num2str(year))
hold on
end


end

for t =1:5
subplot(2,3,t)
xlabel('Time (h)'),ylabel('Loading MVA')
title( sprintf('T%d',t) )
xlim([0,23])
xticks([0:6:18,23])
plot([0 23], [data{t,3},data{t,3}],'k--', ...
    'DisplayName', 'Limit')

end
legend show

set(gcf,'Position',[584 319 792 659])

% reset_subplot(2,3, [0.2 0.7;0.2 0.65])





