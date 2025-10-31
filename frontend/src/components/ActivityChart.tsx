import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  TooltipProps,
} from 'recharts'
import { CommitActivity } from '../lib/api'
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card'

interface ActivityChartProps {
  data: CommitActivity[]
}

function CustomTooltip({ active, payload }: TooltipProps<number, string>) {
  if (active && payload && payload.length) {
    return (
      <div className="bg-card border rounded-lg p-3 shadow-lg">
        <p className="text-sm font-medium">{payload[0].payload.date}</p>
        <p className="text-sm text-primary">
          {payload[0].value} commit{payload[0].value !== 1 ? 's' : ''}
        </p>
      </div>
    )
  }
  return null
}

export default function ActivityChart({ data }: ActivityChartProps) {
  if (!data || data.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Commit Activity</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground text-center py-8">
            No commit activity found for this time period
          </p>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Commit Activity</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis
              dataKey="date"
              className="text-xs"
              tick={{ fill: 'currentColor' }}
            />
            <YAxis className="text-xs" tick={{ fill: 'currentColor' }} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="count" fill="hsl(var(--primary))" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}

