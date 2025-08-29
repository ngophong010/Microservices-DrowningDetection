{{- define "kafka-chart.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{- define "kafka-chart.labels" -}}
helm.sh/chart: {{ include "kafka-chart.chart" . }}
{{ include "kafka-chart.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "kafka-chart.chart" -}}
{{ .Chart.Name }}-{{ .Chart.Version }}
{{- end }}

{{- define "kafka-chart.selectorLabels" -}}
app.kubernetes.io/name: {{ include "kafka-chart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "kafka-chart.name" -}}
{{ .Chart.Name }}
{{- end }}